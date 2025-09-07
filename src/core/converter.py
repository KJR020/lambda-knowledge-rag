"""Scrapbox to Markdown converter."""

import re
from typing import Any
from urllib.parse import quote


class ScrapboxMarkdownConverter:
    """Converts Scrapbox markup to Markdown format."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.base_url = f"https://scrapbox.io/{project_name}"

    def convert(self, scrapbox_text: str, page_metadata: dict[str, Any] = None) -> str:
        """Convert Scrapbox markup to Markdown."""
        if not scrapbox_text:
            return ""

        lines = scrapbox_text.split('\n')
        markdown_lines = []

        for line in lines:
            converted_line = self._convert_line(line)
            markdown_lines.append(converted_line)

        markdown_content = '\n'.join(markdown_lines)

        if page_metadata:
            return self._add_frontmatter(markdown_content, page_metadata)

        return markdown_content

    def _convert_line(self, line: str) -> str:
        """Convert a single line from Scrapbox markup to Markdown."""
        if not line.strip():
            return line

        # Headers: [* text] -> # text
        line = self._convert_headers(line)

        # Links: [[page name]] -> [page name](url)
        line = self._convert_links(line)

        # Code blocks: code:python -> ```python
        line = self._convert_code_blocks(line)

        return line

    def _convert_headers(self, line: str) -> str:
        """Convert Scrapbox headers to Markdown headers."""
        # Pattern: [* text] or [** text] etc.
        pattern = r'^\s*\[(\*+)\s+([^\]]+)\]'
        match = re.match(pattern, line)

        if match:
            level = len(match.group(1))  # Number of asterisks
            text = match.group(2).strip()
            # Convert to markdown header (limit to 6 levels)
            header_level = min(level, 6)
            return '#' * header_level + ' ' + text

        return line

    def _convert_links(self, line: str) -> str:
        """Convert Scrapbox links to Markdown links."""
        # Pattern: [[page name]]
        pattern = r'\[\[([^\]]+)\]\]'

        def replace_link(match):
            page_name = match.group(1)
            # URL encode the page name for the link
            encoded_name = quote(page_name)
            url = f"{self.base_url}/{encoded_name}"
            return f"[{page_name}]({url})"

        return re.sub(pattern, replace_link, line)

    def _convert_code_blocks(self, line: str) -> str:
        """Convert Scrapbox code blocks to Markdown code blocks."""
        # Pattern: code:language
        if line.strip().startswith('code:'):
            language = line.strip()[5:]  # Remove 'code:' prefix
            return f"```{language}"

        return line

    def _add_frontmatter(self, content: str, metadata: dict[str, Any]) -> str:
        """Add YAML frontmatter to the markdown content."""
        frontmatter_lines = ["---"]

        if 'title' in metadata:
            frontmatter_lines.append(f"title: {metadata['title']}")

        if 'id' in metadata:
            page_id = metadata['id']
            title = metadata.get('title', '')
            encoded_title = quote(title) if title else page_id
            url = f"{self.base_url}/{encoded_title}"
            frontmatter_lines.append(f"url: {url}")
            frontmatter_lines.append(f"page_id: {page_id}")

        if 'updated' in metadata:
            # Convert timestamp to ISO format
            import datetime
            timestamp = datetime.datetime.fromtimestamp(
                metadata['updated'], tz=datetime.UTC
            )
            frontmatter_lines.append(
                f"updated_at: {timestamp.isoformat().replace('+00:00', 'Z')}"
            )

        frontmatter_lines.append("---")
        frontmatter_lines.append("")  # Empty line after frontmatter

        # Add title as main header if available
        if 'title' in metadata:
            frontmatter_lines.append(f"# {metadata['title']}")
            frontmatter_lines.append("")  # Empty line after title

        return '\n'.join(frontmatter_lines) + content
