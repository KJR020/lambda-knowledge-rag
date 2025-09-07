"""Scrapbox ETL Lambda handler."""

import json
import logging
from datetime import datetime
from typing import Any

from core.clients import S3Client, ScrapboxClient
from core.config import CONFIG
from core.converter import ScrapboxMarkdownConverter

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context: Any) -> dict:
    """Scrapbox ETL Lambda function entry point."""
    logger.info("Starting Scrapbox ETL process")
    logger.info("Event: %s", json.dumps(event))

    try:
        # Initialize clients
        scrapbox_client = ScrapboxClient()
        s3_client = S3Client()
        converter = ScrapboxMarkdownConverter(CONFIG.scrapbox_project)

        # Get all pages from Scrapbox
        logger.info("Fetching pages from Scrapbox project: %s", CONFIG.scrapbox_project)
        pages = scrapbox_client.get_pages()
        logger.info("Found %d pages", len(pages))

        # Process each page
        processed_count = 0
        errors = []
        metadata_summary = {
            "project": CONFIG.scrapbox_project,
            "processed_at": datetime.utcnow().isoformat() + "Z",
            "total_pages": len(pages),
            "pages": []
        }

        for page in pages:
            try:
                processed_count += 1
                page_id = page.get('id')
                title = page.get('title', f'page-{page_id}')

                logger.info(
                    "Processing page %d/%d: %s", processed_count, len(pages), title
                )

                # Get page content
                page_content = scrapbox_client.get_page_content(title)

                # Extract text content (lines joined)
                lines = page_content.get('lines', [])
                scrapbox_text = '\n'.join(line.get('text', '') for line in lines)

                # Convert to markdown
                page_metadata = {
                    'id': page_id,
                    'title': title,
                    'updated': page.get('updated', 0)
                }

                markdown_content = converter.convert(scrapbox_text, page_metadata)

                # Generate safe filename
                safe_filename = _generate_safe_filename(title)
                s3_key = f"pages/{safe_filename}.md"

                # Upload to S3
                s3_client.upload_markdown_file(
                    bucket=CONFIG.s3_bucket,
                    key=s3_key,
                    content=markdown_content
                )

                # Add to metadata summary
                metadata_summary["pages"].append({
                    "id": page_id,
                    "title": title,
                    "filename": f"{safe_filename}.md",
                    "s3_key": s3_key,
                    "updated": page.get('updated', 0)
                })

                logger.info("Successfully processed: %s -> %s", title, s3_key)

            except Exception as e:
                error_msg = f"Failed to process page {title}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Upload metadata summary
        s3_client.upload_metadata_file(
            bucket=CONFIG.s3_bucket,
            key="pages/metadata.json",
            metadata=metadata_summary
        )

        # Prepare response
        success_count = processed_count - len(errors)
        response = {
            "statusCode": 200,
            "body": {
                "message": "Scrapbox ETL completed",
                "total_pages": len(pages),
                "successful": success_count,
                "failed": len(errors),
                "errors": errors[:10]  # Limit errors in response
            }
        }

        logger.info(
            "ETL completed: %d successful, %d failed", success_count, len(errors)
        )
        return response

    except Exception as e:
        logger.error("ETL process failed: %s", str(e))
        return {
            "statusCode": 500,
            "body": {
                "error": "ETL process failed",
                "message": str(e)
            }
        }


def _generate_safe_filename(title: str) -> str:
    """Generate a safe filename from page title."""
    import re

    # Replace unsafe characters with underscores
    safe_name = re.sub(r'[^\w\s-]', '_', title)
    # Replace spaces and multiple underscores with single underscore
    safe_name = re.sub(r'[\s_]+', '_', safe_name)
    # Remove leading/trailing underscores
    safe_name = safe_name.strip('_')
    # Limit length
    if len(safe_name) > 100:
        safe_name = safe_name[:100]

    return safe_name or 'untitled'
