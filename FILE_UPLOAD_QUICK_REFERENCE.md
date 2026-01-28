# Quick Reference: File Upload Feature

## What Was Added? 🎬📸📄

### File Types Supported:
| Type | Max Size | Formats | Endpoint |
|------|----------|---------|----------|
| **Thumbnails** | 5 MB | JPG, PNG, WebP | `/uploads/thumbnail/{course_id}` |
| **Videos** | 500 MB | MP4, MOV, AVI, MKV | `/uploads/video/{course_id}` |
| **Materials** | 50 MB | PDF, Word, Excel, TXT | `/uploads/material/{course_id}` |

## Where to Use?

### 1. **Creating a Course** (Frontend)
- Go to: `http://localhost:3001/admin/courses/create`
- Fill course details
- Click "Create Course"
- Upload thumbnail image (optional)
- Click "Finish"

### 2. **Files Saved** (Backend)
- Location: `/backend/uploads/`
- Structure:
  ```
  uploads/
  ├── videos/
  ├── thumbnails/
  └── materials/
  ```

### 3. **Access Uploaded Files**
```
http://localhost:8000/uploads/thumbnails/filename.jpg
http://localhost:8000/uploads/videos/filename.mp4
http://localhost:8000/uploads/materials/filename.pdf
```

## API Endpoints

### Upload Thumbnail
```bash
POST /api/v1/uploads/thumbnail/{course_id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

Response: {
  "url": "/uploads/thumbnails/uuid.jpg",
  "filename": "uuid.jpg",
  "original_name": "my-thumbnail.jpg",
  "size": 2048576
}
```

### Upload Video
```bash
POST /api/v1/uploads/video/{course_id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

Response: {
  "url": "/uploads/videos/uuid.mp4",
  "filename": "uuid.mp4",
  "original_name": "lesson-1.mp4",
  "size": 104857600
}
```

### Upload Material
```bash
POST /api/v1/uploads/material/{course_id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

Response: {
  "url": "/uploads/materials/uuid.pdf",
  "filename": "uuid.pdf",
  "original_name": "notes.pdf",
  "size": 5242880
}
```

## Frontend Component

### FileUpload Component
Location: `/frontend/app/components/FileUpload.tsx`

Usage:
```tsx
import FileUpload from '@/components/FileUpload';

<FileUpload
  courseId={123}
  uploadType="thumbnail" // or 'video' or 'material'
  onUploadComplete={(url, filename) => console.log(url)}
  onError={(error) => console.log(error)}
/>
```

## Key Features ✨

✅ **Real-time Progress**: See upload percentage  
✅ **File Validation**: Auto-checks type & size  
✅ **Secure**: Only instructors can upload for their courses  
✅ **Error Handling**: Clear error messages  
✅ **Auto-save**: Thumbnail automatically updates course  
✅ **Preview**: See thumbnail after upload  

## Common Issues & Solutions

### ❌ "File type not allowed"
- Check the file format is correct
- Thumbnails: JPG, PNG, WebP only
- Videos: MP4, MOV, AVI, MKV only
- Materials: PDF, Word, Excel, TXT only

### ❌ "File size exceeds maximum limit"
- Reduce file size or compress
- Thumbnails: Max 5MB (compress images)
- Videos: Max 500MB (use quality compression)
- Materials: Max 50MB (split large files)

### ❌ "Only the course instructor can upload"
- Make sure you're logged in as the course creator
- Admin cannot upload for instructor courses

### ❌ "Failed to save file"
- Check disk space available
- Ensure `/uploads` directory exists and is writable
- Check file permissions

## Testing Locally

### Using the Frontend UI:
1. Login as instructor or admin
2. Go to `/admin/courses/create`
3. Fill course form
4. Click "Create Course"
5. Upload thumbnail image
6. Click "Finish"

### Using cURL:
```bash
# Get your token first
TOKEN="your_access_token"
COURSE_ID=1

# Upload thumbnail
curl -X POST http://localhost:8000/api/v1/uploads/thumbnail/$COURSE_ID \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./my-image.jpg"

# Upload video
curl -X POST http://localhost:8000/api/v1/uploads/video/$COURSE_ID \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./my-video.mp4"

# Upload material
curl -X POST http://localhost:8000/api/v1/uploads/material/$COURSE_ID \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./my-notes.pdf"
```

## File Structure

**Backend Changes:**
- ✅ New: `/backend/app/api/endpoints/uploads.py` - Upload handlers
- ✅ Updated: `/backend/app/api/__init__.py` - Register router
- ✅ Updated: `/backend/main.py` - Static file serving

**Frontend Changes:**
- ✅ New: `/frontend/app/components/FileUpload.tsx` - Upload component
- ✅ Updated: `/frontend/app/admin/courses/create/page.tsx` - Two-step form

**Documentation:**
- ✅ New: `/FILE_UPLOAD_FEATURE.md` - Full implementation details
- ✅ Updated: `/API_DOCUMENTATION.md` - API endpoints

## Next Steps

To add video uploads in lessons:
1. Create lesson form
2. Use `FileUpload` component with `uploadType="video"`
3. Save video URL to lesson record
4. Display video player in lesson view

To add material uploads:
1. Create materials management page
2. Use `FileUpload` component with `uploadType="material"`
3. List materials with download links
4. Track material access

## Performance Tips

- **Compress images** before uploading thumbnails
- **Use lower quality** for demo videos
- **Split large videos** into multiple files
- **Consider CDN** for production use
- **Enable gzip** compression (already enabled)

## Security Checklist

✅ Authorization verified (instructors only)  
✅ File types validated  
✅ File sizes limited  
✅ Filenames randomized (no path traversal)  
✅ Static files properly served  
✅ Error messages don't expose paths  

---

**Need help?** Check the full documentation in `FILE_UPLOAD_FEATURE.md`
