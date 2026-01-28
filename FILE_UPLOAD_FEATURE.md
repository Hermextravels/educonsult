# File Upload Feature - Implementation Summary

## Overview
Added comprehensive file upload functionality for courses, supporting video uploads, image thumbnails, and course materials.

## Backend Implementation

### New Endpoint: `/backend/app/api/endpoints/uploads.py`
Created a dedicated upload handler with three main endpoints:

#### 1. **POST /uploads/thumbnail/{course_id}**
- Upload course thumbnail images
- Max size: 5MB
- Allowed formats: JPG, PNG, WebP
- Auto-updates course thumbnail_url in database
- Returns: `{filename, url, original_name, size}`

#### 2. **POST /uploads/video/{course_id}**
- Upload lesson/course videos
- Max size: 500MB
- Allowed formats: MP4, MOV, AVI, MKV
- Returns: `{filename, url, original_name, size}`

#### 3. **POST /uploads/material/{course_id}**
- Upload course materials (PDFs, documents, etc.)
- Max size: 50MB
- Allowed formats: PDF, Word, Excel, TXT
- Returns: `{filename, url, original_name, size}`

### Features
✅ File validation (type & size)  
✅ Unique filename generation using UUID  
✅ Secure file storage in `/uploads` directory  
✅ Automatic directory creation  
✅ Static file serving via FastAPI  
✅ Authorization check (only course instructors can upload)  

### Directory Structure
```
uploads/
├── videos/      # Lesson videos (up to 500MB each)
├── thumbnails/  # Course thumbnails (up to 5MB each)
└── materials/   # Course materials (up to 50MB each)
```

## Frontend Implementation

### New Component: `/frontend/app/components/FileUpload.tsx`
Reusable file upload component with:
- Drag-and-drop interface
- Progress tracking
- Real-time upload percentage
- Error handling
- Token-based authentication
- XMLHttpRequest for streaming uploads

### Updated Page: `/frontend/app/admin/courses/create/page.tsx`
Enhanced course creation flow:
1. **Step 1**: Fill course details and click "Create Course"
2. **Step 2**: System creates course and shows file upload section
3. **Step 3**: Upload thumbnail image (optional, can be done later)
4. **Step 4**: Click "Finish" to complete

Features:
- Two-step form process
- Thumbnail preview after upload
- Real-time upload status
- Validation feedback

## API Integration

### Updated: `/backend/app/api/__init__.py`
- Registered uploads router with API

### Updated: `/backend/main.py`
- Mounted `/uploads` as static file directory
- Enables public file serving at `/uploads/{category}/{filename}`

## File Serving

Uploaded files are accessible via:
```
http://localhost:8000/uploads/thumbnails/{filename}
http://localhost:8000/uploads/videos/{filename}
http://localhost:8000/uploads/materials/{filename}
```

## Usage Example

### Creating a course with thumbnail:

1. **Create course**:
   ```bash
   POST /api/v1/courses/
   {
     "title": "Python Basics",
     "slug": "python-basics",
     "description": "Learn Python",
     "category": "Programming",
     "price": 29.99
   }
   ```

2. **Upload thumbnail**:
   ```bash
   POST /api/v1/uploads/thumbnail/1
   Content-Type: multipart/form-data
   Authorization: Bearer {token}
   
   file: <binary image data>
   ```

3. **Response**:
   ```json
   {
     "filename": "uuid.jpg",
     "url": "/uploads/thumbnails/uuid.jpg",
     "original_name": "course.jpg",
     "size": 2048576
   }
   ```

## Security Features

✅ **Authorization**: Only course instructors can upload  
✅ **File Validation**: Type and size checking  
✅ **Secure Storage**: UUID-based filenames (no path traversal)  
✅ **Token Authentication**: JWT-based API access  
✅ **Error Handling**: Graceful error messages  

## Error Handling

**Invalid file type**:
```json
{
  "detail": "File type not allowed. Allowed types: {...}"
}
```

**File too large**:
```json
{
  "detail": "File size exceeds maximum limit of 500MB"
}
```

**Not authorized**:
```json
{
  "detail": "Only the course instructor can upload videos"
}
```

## Next Steps (Optional Enhancements)

1. **Video Processing**:
   - FFmpeg integration for video transcoding
   - Thumbnail generation from videos
   - HLS streaming for adaptive quality

2. **Chunked Uploads**:
   - Support for resume on failure
   - Better handling of large files

3. **Virus Scanning**:
   - ClamAV or similar for uploaded files
   - Security scanning before serving

4. **CDN Integration**:
   - CloudFlare or similar for faster delivery
   - Automatic caching

5. **Progress Dashboard**:
   - Show upload progress for all files
   - File management interface

## Testing

### Frontend Upload (Dev Tools):
```javascript
// Test in browser console
const file = new File(['content'], 'test.pdf', {type: 'application/pdf'});
const formData = new FormData();
formData.append('file', file);
fetch('http://localhost:8000/api/v1/uploads/material/1', {
  method: 'POST',
  headers: {Authorization: `Bearer ${localStorage.getItem('accessToken')}`},
  body: formData
}).then(r => r.json()).then(console.log);
```

### API Testing (cURL):
```bash
curl -X POST http://localhost:8000/api/v1/uploads/thumbnail/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@path/to/image.jpg"
```
