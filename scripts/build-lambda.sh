#!/bin/bash

# Lambda deployment package builder using uv

set -e

PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")
BUILD_DIR="$PROJECT_ROOT/build"
PACKAGE_FILE="$PROJECT_ROOT/lambda-package.zip"

echo "Building Lambda package..."

# Clean up previous build
rm -rf "$BUILD_DIR"
rm -f "$PACKAGE_FILE"

# Create build directory
mkdir -p "$BUILD_DIR"

# Copy source code
cp -r "$PROJECT_ROOT/src/"* "$BUILD_DIR/"

# Install dependencies using uv
cd "$PROJECT_ROOT"
echo "Installing dependencies with uv..."
uv pip install --target "$BUILD_DIR" boto3 pydantic requests --no-deps

# Create deployment package
cd "$BUILD_DIR"
zip -r "$PACKAGE_FILE" .

cd "$PROJECT_ROOT"
rm -rf "$BUILD_DIR"

echo "Lambda package created: $PACKAGE_FILE"
echo "Package size: $(du -h "$PACKAGE_FILE" | cut -f1)"