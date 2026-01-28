'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  category: string;
  level: string;
  price: number;
  is_published: boolean;
  thumbnail_url?: string;
  students_count?: number;
}

export default function CourseManagement() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState<Course[]>([]);
  const [userRole, setUserRole] = useState<string>('');

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    const role = localStorage.getItem('userRole');

    if (!token) {
      router.push('/login');
      return;
    }

    if (role !== 'admin' && role !== 'instructor') {
      router.push('/dashboard');
      return;
    }

    setUserRole(role);
    fetchCourses(token);
  }, [router]);

  const fetchCourses = async (token: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/courses/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setCourses(data);
      }
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (courseId: number) => {
    if (!confirm('Are you sure you want to delete this course?')) return;

    const token = localStorage.getItem('accessToken');
    try {
      const response = await fetch(`http://localhost:8000/api/v1/courses/${courseId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setCourses(courses.filter((c) => c.id !== courseId));
        alert('Course deleted successfully');
      } else {
        alert('Failed to delete course');
      }
    } catch (error) {
      console.error('Error deleting course:', error);
      alert('Error deleting course');
    }
  };

  const togglePublish = async (courseId: number, currentStatus: boolean) => {
    const token = localStorage.getItem('accessToken');
    try {
      const response = await fetch(`http://localhost:8000/api/v1/courses/${courseId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ is_published: !currentStatus }),
      });

      if (response.ok) {
        const updatedCourse = await response.json();
        setCourses(courses.map((c) => (c.id === courseId ? updatedCourse : c)));
      }
    } catch (error) {
      console.error('Error updating course:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading courses...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Course Management
            </h1>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              Manage all your courses
            </p>
          </div>
          <Link
            href="/admin/courses/create"
            className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700"
          >
            + Create New Course
          </Link>
        </div>

        {/* Courses List */}
        {courses.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">📚</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              No Courses Yet
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Get started by creating your first course
            </p>
            <Link
              href="/admin/courses/create"
              className="inline-block px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700"
            >
              Create Course
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {courses.map((course) => (
              <div
                key={course.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                          {course.title}
                        </h3>
                        <span
                          className={`px-3 py-1 text-xs font-medium rounded-full ${
                            course.is_published
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                          }`}
                        >
                          {course.is_published ? 'Published' : 'Draft'}
                        </span>
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mb-4">
                        {course.description}
                      </p>
                      <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                        <span>📂 {course.category}</span>
                        <span>📊 {course.level}</span>
                        <span>💰 ${course.price}</span>
                        <span>👥 {course.students_count || 0} students</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => togglePublish(course.id, course.is_published)}
                        className={`px-4 py-2 text-sm font-medium rounded-lg ${
                          course.is_published
                            ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200 dark:bg-yellow-900 dark:text-yellow-200'
                            : 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900 dark:text-green-200'
                        }`}
                      >
                        {course.is_published ? 'Unpublish' : 'Publish'}
                      </button>
                      <Link
                        href={`/admin/courses/${course.id}/edit`}
                        className="px-4 py-2 text-sm font-medium bg-blue-100 text-blue-800 rounded-lg hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-200"
                      >
                        Edit
                      </Link>
                      <button
                        onClick={() => handleDelete(course.id)}
                        className="px-4 py-2 text-sm font-medium bg-red-100 text-red-800 rounded-lg hover:bg-red-200 dark:bg-red-900 dark:text-red-200"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
