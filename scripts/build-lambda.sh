#!/bin/bash

# Lambda deployment package builder using uv

set -e

PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")
BUILD_TEMP_DIR="$PROJECT_ROOT/build/temp"
OUTPUT_DIR="$PROJECT_ROOT/build/lambda"
PACKAGE_FILE="$OUTPUT_DIR/deployment.zip"

echo "Building Lambda package..."

# Clean up previous build
rm -rf "$BUILD_TEMP_DIR"
rm -rf "$OUTPUT_DIR"

# Create build directories
mkdir -p "$BUILD_TEMP_DIR"
mkdir -p "$OUTPUT_DIR"

# Copy source code
cp -r "$PROJECT_ROOT/src/"* "$BUILD_TEMP_DIR/"

# Install dependencies using uv
cd "$PROJECT_ROOT"
echo "Installing dependencies with uv..."
uv pip install --target "$BUILD_TEMP_DIR" boto3 pydantic requests --no-deps

# Create deployment package
cd "$BUILD_TEMP_DIR"
zip -r "$PACKAGE_FILE" .

# Clean up temp directory
cd "$PROJECT_ROOT"
rm -rf "$BUILD_TEMP_DIR"

echo "Lambda package created: $PACKAGE_FILE"
echo "Package size: $(du -h "$PACKAGE_FILE" | cut -f1)"