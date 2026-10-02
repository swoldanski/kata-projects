# Kata 4: File Upload

Source: https://github.com/devdrops/Katas/tree/kata-upload-file

## Problem

Build a robust file upload handler with validation, storage, and processing.

## Goals

- Handle multipart/form-data
- Validate file type, size, content
- Secure storage (random names, outside web root)
- Progress tracking
- Chunked/resumable uploads

## Features

1. **Validation**: MIME type, extension, magic bytes, size limits
2. **Storage**: local, S3, cloud storage abstraction
3. **Naming**: UUID, hash-based, preserve original
4. **Processing**: image resize, thumbnail, virus scan
5. **Metadata**: store in DB (original name, size, type, path)
6. **Cleanup**: temp files, failed uploads, orphaned files

## Examples

```python
# File upload
handler = FileUploadHandler(storage=LocalStorage("/uploads"))
result = handler.upload(file, allowed_types=["image/*"], max_size=5_000_000)
# => {"path": "/uploads/abc123.jpg", "size": 1024, "mime": "image/jpeg"}
```

## Exercises

1. Basic single file upload
2. Multiple files
3. Image validation (dimensions, type)
4. Chunked upload (resumable)
5. Progress API (WebSocket/SSE)
6. Image processing pipeline
7. Antivirus integration
8. CDN integration
9. Upload permissions/ACL