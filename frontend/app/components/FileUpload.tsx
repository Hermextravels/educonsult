'use client';

import { useState } from 'react';

interface FileUploadProps {
  courseId: number;
  uploadType: 'video' | 'thumbnail' | 'material';
  onUploadComplete: (url: string, filename: string) => void;
  onError: (error: string) => void;
}

export default function FileUpload({
  courseId,
  uploadType,
  onUploadComplete,
  onError,
}: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const getUploadConfig = () => {
    switch (uploadType) {
      case 'video':
        return {
          endpoint: `/api/v1/uploads/video/${courseId}`,
          accept: 'video/*',
          label: 'Upload Video',
          hint: 'Max 500MB (MP4, MOV, AVI, MKV)',
        };
      case 'thumbnail':
        return {
          endpoint: `/api/v1/uploads/thumbnail/${courseId}`,
          accept: 'image/*',
          label: 'Upload Thumbnail',
          hint: 'Max 5MB (JPG, PNG, WebP)',
        };
      case 'material':
        return {
          endpoint: `/api/v1/uploads/material/${courseId}`,
          accept: '.pdf,.doc,.docx,.xls,.xlsx,.txt',
          label: 'Upload Material',
          hint: 'Max 50MB (PDF, Word, Excel, TXT)',
        };
    }
  };

  const config = getUploadConfig();

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        onError('Authentication token not found');
        setUploading(false);
        return;
      }

      const xhr = new XMLHttpRequest();

      // Track upload progress
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const percentComplete = (e.loaded / e.total) * 100;
          setProgress(percentComplete);
        }
      });

      xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          onUploadComplete(response.url, response.filename);
          setProgress(0);
        } else {
          const error = JSON.parse(xhr.responseText);
          onError(error.detail || 'Upload failed');
        }
        setUploading(false);
      });

      xhr.addEventListener('error', () => {
        onError('Network error during upload');
        setUploading(false);
      });

      xhr.open('POST', `http://localhost:8000${config.endpoint}`);
      xhr.setRequestHeader('Authorization', `Bearer ${token}`);
      xhr.send(formData);
    } catch (err) {
      onError('Upload failed');
      setUploading(false);
    }
  };

  return (
    <div className="space-y-2">
      <label className="block">
        <span className="sr-only">{config.label}</span>
        <div className="relative">
          <input
            type="file"
            accept={config.accept}
            onChange={handleFileChange}
            disabled={uploading}
            className="sr-only"
            id={`file-input-${uploadType}`}
          />
          <label
            htmlFor={`file-input-${uploadType}`}
            className={`flex items-center justify-center px-4 py-3 border-2 border-dashed rounded-lg cursor-pointer transition ${
              uploading
                ? 'border-gray-300 bg-gray-50 cursor-not-allowed'
                : 'border-indigo-300 bg-indigo-50 hover:border-indigo-500 hover:bg-indigo-100'
            }`}
          >
            <div className="text-center">
              <span className="text-2xl mb-2 block">📁</span>
              <span className="text-sm font-semibold text-indigo-600">
                {uploading ? `Uploading... ${progress.toFixed(0)}%` : config.label}
              </span>
              <p className="text-xs text-gray-600 mt-1">{config.hint}</p>
            </div>
          </label>
        </div>
      </label>

      {/* Progress Bar */}
      {uploading && (
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-indigo-600 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}
