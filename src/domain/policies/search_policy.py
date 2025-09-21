"""
検索に関するドメインポリシー
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class SearchPolicy:
    """検索結果のフィルタリングとランキングポリシー"""

    @staticmethod
    def filter_results(
        results: list[dict[str, Any]], min_score: float = 0.1
    ) -> list[dict[str, Any]]:
        """
        検索結果をフィルタリング

        Args:
            results: 検索結果のリスト
            min_score: 最小スコア閾値

        Returns:
            フィルタリングされた結果
        """
        filtered = []

        for result in results:
            score = result.get("score", 0.0)

            # スコアが閾値以下の場合は除外
            if score < min_score:
                logger.debug(f"Filtered out result with low score: {score}")
                continue

            # 空のコンテンツは除外
            content = result.get("content", "").strip()
            if not content:
                logger.debug("Filtered out result with empty content")
                continue

            filtered.append(result)

        return filtered

    @staticmethod
    def boost_recent_documents(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        最近のドキュメントのスコアをブースト

        Args:
            results: 検索結果のリスト

        Returns:
            ブーストされた結果
        """
        boosted_results = []
        current_time = datetime.utcnow()

        for result in results:
            # メタデータから更新日時を取得
            metadata = result.get("metadata", {})
            updated_at_str = metadata.get("updated_at")

            boost_factor = 1.0

            if updated_at_str:
                try:
                    # Unix timestampの場合
                    if isinstance(updated_at_str, (int, float)):
                        updated_at = datetime.fromtimestamp(updated_at_str)
                    else:
                        # ISO形式の場合
                        updated_at = datetime.fromisoformat(
                            updated_at_str.replace("Z", "+00:00")
                        )

                    # 経過日数を計算
                    days_ago = (current_time - updated_at).days

                    # 最近のドキュメントほど高いブーストを適用
                    if days_ago <= 7:
                        boost_factor = 1.3  # 1週間以内
                    elif days_ago <= 30:
                        boost_factor = 1.2  # 1ヶ月以内
                    elif days_ago <= 90:
                        boost_factor = 1.1  # 3ヶ月以内

                except (ValueError, TypeError):
                    logger.warning(f"Invalid date format: {updated_at_str}")

            # スコアをブースト
            original_score = result.get("score", 0.0)
            boosted_score = original_score * boost_factor

            result_copy = result.copy()
            result_copy["score"] = boosted_score
            result_copy["boost_factor"] = boost_factor

            boosted_results.append(result_copy)

        return boosted_results

    @staticmethod
    def remove_duplicates(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        重複するドキュメントを除去

        Args:
            results: 検索結果のリスト

        Returns:
            重複除去された結果
        """
        seen_ids = set()
        unique_results = []

        for result in results:
            doc_id = result.get("id")
            if not doc_id:
                # IDがない場合はコンテンツで判定
                content = result.get("content", "")[:100]  # 最初の100文字で判定
                doc_id = hash(content)

            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                unique_results.append(result)
            else:
                logger.debug(f"Removed duplicate document: {doc_id}")

        return unique_results

    @staticmethod
    def rank_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        検索結果をランキング

        Args:
            results: 検索結果のリスト

        Returns:
            ランキングされた結果
        """
        # スコアでソート（降順）
        ranked = sorted(results, key=lambda x: x.get("score", 0.0), reverse=True)

        # ランキング情報を追加
        for i, result in enumerate(ranked):
            result["rank"] = i + 1

        return ranked

    @classmethod
    def apply_search_policies(
        cls,
        results: list[dict[str, Any]],
        min_score: float = 0.1,
        boost_recent: bool = True,
        remove_dups: bool = True,
    ) -> list[dict[str, Any]]:
        """
        すべての検索ポリシーを適用

        Args:
            results: 検索結果のリスト
            min_score: 最小スコア閾値
            boost_recent: 最近のドキュメントをブーストするかどうか
            remove_dups: 重複を除去するかどうか

        Returns:
            ポリシーが適用された結果
        """
        processed_results = results.copy()

        # 1. フィルタリング
        processed_results = cls.filter_results(processed_results, min_score)

        # 2. 重複除去
        if remove_dups:
            processed_results = cls.remove_duplicates(processed_results)

        # 3. 最近のドキュメントをブースト
        if boost_recent:
            processed_results = cls.boost_recent_documents(processed_results)

        # 4. ランキング
        processed_results = cls.rank_results(processed_results)

        logger.info(
            f"Applied search policies: {len(results)} -> {len(processed_results)} results"
        )

        return processed_results
