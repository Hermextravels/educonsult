'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import FileUpload from '../../../components/FileUpload';

export default function CreateCourse() {
  const router = useRouter();
  const [courseId, setCourseId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    description: '',
    category: '',
    level: 'beginner',
    price: '0',
    currency: 'NGN',
    is_free: true,
    duration_hours: '',
    thumbnail_url: '',
    learning_objectives: '',
    requirements: '',
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));

    // Auto-generate slug from title
    if (name === 'title') {
      const slug = value
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '');
      setFormData((prev) => ({ ...prev, slug }));
    }

    // Update price based on is_free
    if (name === 'is_free') {
      setFormData((prev) => ({ ...prev, price: checked ? '0' : prev.price }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const token = localStorage.getItem('accessToken');
    if (!token) {
      router.push('/login');
      return;
    }

    // Prepare data
    const courseData = {
      title: formData.title,
      slug: formData.slug,
      description: formData.description,
      category: formData.category,
      level: formData.level,
      price: parseFloat(formData.price),
      currency: formData.currency,
      is_free: formData.is_free,
      duration_hours: formData.duration_hours ? parseFloat(formData.duration_hours) : null,
      thumbnail_url: formData.thumbnail_url || null,
      learning_objectives: formData.learning_objectives
        ? formData.learning_objectives.split('\n').filter((obj) => obj.trim())
        : [],
      requirements: formData.requirements
        ? formData.requirements.split('\n').filter((req) => req.trim())
        : [],
    };

    try {
      const response = await fetch('http://localhost:8000/api/v1/courses/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(courseData),
      });

      if (response.ok) {
        const data = await response.json();
        setCourseId(data.id);
        setError('');
        setUploadSuccess('Course created successfully! Now you can upload media files below.');
        // Scroll to upload section
        setTimeout(() => {
          const uploadSection = document.getElementById('upload-section');
          if (uploadSection) {
            uploadSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create course');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleThumbnailUpload = (url: string, filename: string) => {
    setFormData((prev) => ({ ...prev, thumbnail_url: url }));
    setUploadSuccess('Thumbnail uploaded successfully!');
  };

  const handleUploadError = (error: string) => {
    setError(error);
  };

  const handleFinish = () => {
    alert('Course created successfully!');
    router.push(`/admin/courses`);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/admin/courses"
            className="text-indigo-600 hover:text-indigo-700 mb-4 inline-block"
          >
            ← Back to Courses
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Create New Course
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Fill in the details below to create a new course
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg">
              <p className="text-red-800 dark:text-red-200">{error}</p>
            </div>
          )}

          {uploadSuccess && (
            <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg">
              <p className="text-green-800 dark:text-green-200 font-semibold">{uploadSuccess}</p>
            </div>
          )}

          {/* Title */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Course Title *
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              placeholder="Introduction to Python Programming"
            />
          </div>

          {/* Slug */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Slug (URL) *
            </label>
            <input
              type="text"
              name="slug"
              value={formData.slug}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              placeholder="introduction-to-python-programming"
            />
            <p className="mt-1 text-sm text-gray-500">Auto-generated from title</p>
          </div>

          {/* Description */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows={5}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              placeholder="Provide a detailed description of your course..."
            />
          </div>

          {/* Category and Level */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Category *
              </label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              >
                <option value="">Select category</option>
                <option value="Programming">Programming</option>
                <option value="Design">Design</option>
                <option value="Business">Business</option>
                <option value="Marketing">Marketing</option>
                <option value="Data Science">Data Science</option>
                <option value="Photography">Photography</option>
                <option value="Music">Music</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Level *
              </label>
              <select
                name="level"
                value={formData.level}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
          </div>

          {/* Price Settings */}
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <input
                type="checkbox"
                name="is_free"
                checked={formData.is_free}
                onChange={handleChange}
                className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-600"
              />
              <label className="ml-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                This is a free course
              </label>
            </div>

            {!formData.is_free && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Price *
                  </label>
                  <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                    required={!formData.is_free}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Currency
                  </label>
                  <select
                    name="currency"
                    value={formData.currency}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
                  >
                    <option value="NGN">NGN (₦)</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="GBP">GBP (£)</option>
                  </select>
                </div>
              </div>
            )}
          </div>

          {/* Duration and Thumbnail */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Duration (hours)
              </label>
              <input
                type="number"
                name="duration_hours"
                value={formData.duration_hours}
                onChange={handleChange}
                min="0"
                step="0.5"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
                placeholder="10.5"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Thumbnail URL
              </label>
              <input
                type="url"
                name="thumbnail_url"
                value={formData.thumbnail_url}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
                placeholder="https://example.com/image.jpg"
              />
            </div>
          </div>

          {/* File Upload Section - Only show after course is created */}
          {courseId && (
            <div 
              id="upload-section"
              className="mb-6 p-8 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 border-2 border-blue-300 dark:border-blue-700 rounded-xl shadow-lg"
            >
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-blue-900 dark:text-blue-200 mb-2">
                  📁 Upload Course Media
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Your course has been created! Now add thumbnails, videos, and materials.
                </p>
              </div>
              <div className="space-y-8">{/* Thumbnail Upload */}
                {/* Thumbnail Upload */}
                <div className="border-b border-blue-200 dark:border-blue-700 pb-6">
                  <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    🖼️ Course Thumbnail
                  </h4>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-3">
                    Upload a course thumbnail image (JPG, PNG, WebP - Max 5MB)
                  </p>
                  <FileUpload
                    courseId={courseId}
                    uploadType="thumbnail"
                    onUploadComplete={handleThumbnailUpload}
                    onError={handleUploadError}
                  />
                  {formData.thumbnail_url && (
                    <div className="mt-3">
                      <p className="text-xs text-green-600 dark:text-green-400 font-semibold">
                        ✓ Thumbnail uploaded successfully!
                      </p>
                      <img 
                        src={`http://localhost:8000${formData.thumbnail_url}`}
                        alt="Thumbnail preview"
                        className="mt-2 h-32 rounded-lg object-cover border border-blue-300"
                      />
                    </div>
                  )}
                </div>

                {/* Video Upload */}
                <div className="border-b border-blue-200 dark:border-blue-700 pb-6">
                  <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    🎬 Lesson Videos
                  </h4>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-3">
                    Upload lesson videos (MP4, MOV, AVI, MKV - Max 500MB each)
                  </p>
                  <FileUpload
                    courseId={courseId}
                    uploadType="video"
                    onUploadComplete={(url, filename) => {
                      setUploadSuccess(`Video uploaded: ${filename}`);
                    }}
                    onError={handleUploadError}
                  />
                  {uploadSuccess.includes('Video') && (
                    <p className="text-xs text-green-600 dark:text-green-400 font-semibold mt-2">
                      ✓ {uploadSuccess}
                    </p>
                  )}
                </div>

                {/* Materials Upload */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    📄 Course Materials
                  </h4>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-3">
                    Upload course materials like PDFs, Word docs, Excel sheets (Max 50MB each)
                  </p>
                  <FileUpload
                    courseId={courseId}
                    uploadType="material"
                    onUploadComplete={(url, filename) => {
                      setUploadSuccess(`Material uploaded: ${filename}`);
                    }}
                    onError={handleUploadError}
                  />
                  {uploadSuccess.includes('Material') && (
                    <p className="text-xs text-green-600 dark:text-green-400 font-semibold mt-2">
                      ✓ {uploadSuccess}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Learning Objectives */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Learning Objectives
            </label>
            <textarea
              name="learning_objectives"
              value={formData.learning_objectives}
              onChange={handleChange}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              placeholder="Enter one objective per line&#10;Master Python basics&#10;Build real-world projects&#10;Understand OOP concepts"
            />
            <p className="mt-1 text-sm text-gray-500">One objective per line</p>
          </div>

          {/* Requirements */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Requirements
            </label>
            <textarea
              name="requirements"
              value={formData.requirements}
              onChange={handleChange}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-600 dark:bg-gray-700 dark:text-white"
              placeholder="Enter one requirement per line&#10;Basic computer skills&#10;Motivation to learn&#10;No prior programming experience needed"
            />
            <p className="mt-1 text-sm text-gray-500">One requirement per line</p>
          </div>

          {/* Submit Buttons */}
          <div className="flex items-center justify-end space-x-4">
            <Link
              href="/admin/courses"
              className="px-6 py-3 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              {courseId ? 'Back to Courses' : 'Cancel'}
            </Link>
            {courseId ? (
              <button
                type="button"
                onClick={handleFinish}
                className="px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700"
              >
                ✓ Finish
              </button>
            ) : (
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Course'}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
