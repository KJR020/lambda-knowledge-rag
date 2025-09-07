FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY . /app

# tox をインストール
RUN uv pip install --system tox

CMD ["tox"]
