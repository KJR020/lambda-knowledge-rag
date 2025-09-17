FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY . /app

# toxを開発依存関係として追加
RUN uv add --dev tox

# 依存関係をインストール
RUN uv sync

CMD ["uv", "run", "tox"]
