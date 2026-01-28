# Comprehensive API Documentation - EduLearn Platform

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer {access_token}
```

## Response Format

All responses follow this format:

```json
{
  "data": {...},
  "message": "Success",
  "status_code": 200
}
```

## Error Handling

Error responses:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Endpoints

### 1. Authentication Endpoints

#### Register User
```
POST /users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "securepassword123"
}

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "student",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-27T10:00:00"
}
```

#### Login
```
POST /users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Refresh Token
```
POST /users/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```
GET /users/me
Authorization: Bearer {token}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "student",
  "is_active": true,
  "avatar_url": "https://...",
  "bio": "User bio",
  "created_at": "2024-01-27T10:00:00"
}
```

#### Update Profile
```
PUT /users/me
Authorization: Bearer {token}
Content-Type: application/json

{
  "full_name": "Updated Name",
  "phone": "+1234567890",
  "bio": "Updated bio",
  "avatar_url": "https://..."
}

Response: 200 OK
{...updated user data...}
```

### 6. File Upload Endpoints

#### Upload Course Thumbnail
```
POST /uploads/thumbnail/{course_id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

body: {
  "file": <binary image data>
}

Max Size: 5MB
Allowed Types: JPG, PNG, WebP

Response: 200 OK
{
  "filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
  "url": "/uploads/thumbnails/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
  "original_name": "course-thumbnail.jpg",
  "size": 2048576
}
```

#### Upload Course Video
```
POST /uploads/video/{course_id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

body: {
  "file": <binary video data>
}

Max Size: 500MB
Allowed Types: MP4, MOV, AVI, MKV

Response: 200 OK
{
  "filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp4",
  "url": "/uploads/videos/a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp4",
  "original_name": "lesson-1.mp4",
  "size": 104857600
}
```

#### Upload Course Materials
```
POST /uploads/material/{course_id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

body: {
  "file": <binary file data>
}

Max Size: 50MB
Allowed Types: PDF, Word (DOC, DOCX), Excel (XLS, XLSX), TXT

Response: 200 OK
{
  "filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.pdf",
  "url": "/uploads/materials/a1b2c3d4-e5f6-7890-abcd-ef1234567890.pdf",
  "original_name": "course-notes.pdf",
  "size": 5242880
}
```



- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently no rate limiting is implemented, but consider adding:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Pagination

List endpoints support pagination with query parameters:
- `skip` (default: 0) - Number of items to skip
- `limit` (default: 20) - Number of items to return

## Filtering

Supported filters vary by endpoint:
- Courses: `category`, `level`
- Users: `role` (admin only)

---

For complete API documentation and testing, visit:
```
http://localhost:8000/api/v1/docs
```
