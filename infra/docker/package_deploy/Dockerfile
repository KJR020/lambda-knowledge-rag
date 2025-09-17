FROM python:3.13-slim

WORKDIR /app

COPY . .

# ビルドコンテキストに関係なく CMD が実行できるよう、デプロイスクリプトをコンテナルートにコピー
COPY src/docker/package_deploy/deploy.sh ./deploy.sh

RUN apt-get update && \
  apt-get install -y unzip sudo curl zip less && \
  rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
  unzip awscliv2.zip && \
  sudo ./aws/install && \
  rm -rf awscliv2.zip aws

# AWS SAM CLIをインストール
RUN curl -Lo "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip" -o "aws-sam-cli.zip" && \
  unzip aws-sam-cli.zip -d sam-installation && \
  sudo ./sam-installation/install && \
  rm -rf aws-sam-cli.zip sam-installation

RUN chmod +x ./deploy.sh

CMD ["./deploy.sh"]
