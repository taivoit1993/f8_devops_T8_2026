#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$DIR/lambda_build"
OUTPUT_ZIP="$DIR/lambda_deployment.zip"

echo "=== 1. Dọn dẹp thư mục build cũ ==="
rm -rf "$BUILD_DIR" "$OUTPUT_ZIP"
mkdir -p "$BUILD_DIR"

echo "=== 2. Cài đặt thư viện bằng Docker cho nền tảng Linux x86_64 (Python 3.14) ==="
docker run --rm --platform linux/amd64 \
  -v "$BUILD_DIR":/var/task \
  python:3.14-slim bash -c "
    pip install --no-cache-dir \
      fastapi \
      mangum \
      pydantic \
      sqlalchemy \
      greenlet \
      asyncpg \
      python-dotenv \
      -t /var/task

    # Dọn dẹp các file cache, test không cần thiết để giảm kích thước zip
    find /var/task -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    find /var/task -type d -name '*.dist-info' -exec rm -rf {} + 2>/dev/null || true
    find /var/task -type f -name '*.pyc' -delete || true
    find /var/task -type f -name '*.so' -exec strip {} + 2>/dev/null || true
  "

echo "=== 3. Sao chép mã nguồn backend vào build ==="
cp "$DIR"/backend/*.py "$BUILD_DIR"/

echo "=== 4. Đóng gói zip file ==="
cd "$BUILD_DIR"
zip -r9 "$OUTPUT_ZIP" .

echo "=== Hoàn tất! File zip đã tạo tại: $OUTPUT_ZIP ==="
ls -lh "$OUTPUT_ZIP"
