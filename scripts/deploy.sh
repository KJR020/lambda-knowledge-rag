#!/bin/bash

# Complete deployment script for Scrapbox ETL system

set -e

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TERRAFORM_DIR="$PROJECT_ROOT/infra/terraform"

echo "🚀 Deploying Scrapbox ETL system..."

# Check prerequisites
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Please install Terraform first."
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI first."
    exit 1
fi

if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Please install uv first."
    exit 1
fi

# Check if terraform.tfvars exists
if [ ! -f "$TERRAFORM_DIR/terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found. Please create it from terraform.tfvars.example"
    echo "📁 Copy: cp $TERRAFORM_DIR/terraform.tfvars.example $TERRAFORM_DIR/terraform.tfvars"
    echo "✏️  Then edit terraform.tfvars with your actual values."
    exit 1
fi

echo "1️⃣ Building Lambda package..."
"$SCRIPT_DIR/build-lambda.sh"

echo "2️⃣ Deploying infrastructure with Terraform..."
cd "$TERRAFORM_DIR"
terraform init
terraform apply -auto-approve

echo "3️⃣ Getting infrastructure outputs..."
LAMBDA_ROLE_ARN=$(terraform output -raw lambda_role_arn)
S3_BUCKET_NAME=$(terraform output -raw s3_bucket_name)
SECRETS_NAME=$(terraform output -raw secrets_manager_secret_name)

echo "4️⃣ Deploying Lambda function..."
cd "$PROJECT_ROOT"

# Check if Lambda function exists
if aws lambda get-function --function-name scrapbox-etl &>/dev/null; then
    echo "📝 Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name scrapbox-etl \
        --zip-file fileb://lambda-package.zip

    aws lambda update-function-configuration \
        --function-name scrapbox-etl \
        --environment Variables="{
            \"AWS_REGION\":\"$(aws configure get region)\",
            \"S3_BUCKET\":\"$S3_BUCKET_NAME\",
            \"SCRAPBOX_SECRET_NAME\":\"$SECRETS_NAME\"
        }"
else
    echo "🆕 Creating new Lambda function..."
    aws lambda create-function \
        --function-name scrapbox-etl \
        --runtime python3.11 \
        --role "$LAMBDA_ROLE_ARN" \
        --handler handlers.scrapbox_etl.lambda_handler \
        --zip-file fileb://lambda-package.zip \
        --timeout 300 \
        --memory-size 512 \
        --environment Variables="{
            \"AWS_REGION\":\"$(aws configure get region)\",
            \"S3_BUCKET\":\"$S3_BUCKET_NAME\",
            \"SCRAPBOX_SECRET_NAME\":\"$SECRETS_NAME\"
        }"
fi

echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Resources created:"
echo "  🔐 IAM Role: $LAMBDA_ROLE_ARN"
echo "  🗄️  S3 Bucket: $S3_BUCKET_NAME"
echo "  🔑 Secret: $SECRETS_NAME"
echo "  ⚡ Lambda: scrapbox-etl"
echo ""
echo "🧪 To test the deployment:"
echo "  aws lambda invoke --function-name scrapbox-etl --payload '{}' response.json"
echo "  cat response.json"