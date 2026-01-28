'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/courses')
      .then(res => res.json())
      .then(data => {
        setCourses(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleEnroll = async (courseId: number, isFree: boolean, price: number) => {
    // Check if user is logged in
    const token = localStorage.getItem('accessToken');
    
    if (!token) {
      alert('Please login to enroll in courses');
      router.push('/login');
      return;
    }

    setEnrolling(courseId);

    try {
      if (isFree || price === 0) {
        // Direct enrollment for free courses
        const response = await fetch(`http://localhost:8000/api/v1/courses/${courseId}/enroll`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          alert('Successfully enrolled! Redirecting to dashboard...');
          router.push('/dashboard');
        } else {
          const error = await response.json();
          alert(error.detail || 'Failed to enroll in course');
        }
      } else {
        // Redirect to payment for paid courses
        alert('Payment integration coming soon! This course requires payment.');
        // TODO: Implement payment flow
        // router.push(`/checkout/${courseId}`);
      }
    } catch (error) {
      console.error('Enrollment error:', error);
      alert('An error occurred during enrollment');
    } finally {
      setEnrolling(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <nav className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-indigo-600">
            🎓 EduConsult
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="text-gray-700 dark:text-gray-300 hover:text-indigo-600">
              Dashboard
            </Link>
            <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-indigo-600">
              Login
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-8">Browse Courses</h1>

        {loading ? (
          <div className="text-center text-gray-600 dark:text-gray-300 py-12">Loading courses...</div>
        ) : courses.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">📚</div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">No Courses Available</h2>
            <p className="text-gray-600 dark:text-gray-300">Check back soon for new courses!</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course: any) => (
              <div key={course.id} className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
                {course.thumbnail_url ? (
                  <img src={course.thumbnail_url} alt={course.title} className="h-48 w-full object-cover" />
                ) : (
                  <div className="h-48 bg-gradient-to-br from-indigo-500 to-purple-600"></div>
                )}
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200">
                      {course.level || 'Beginner'}
                    </span>
                    {course.category && (
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200">
                        {course.category}
                      </span>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{course.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4 line-clamp-2">{course.description}</p>
                  {course.duration_hours && (
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                      📚 {course.duration_hours} hours
                    </p>
                  )}
                  <div className="flex justify-between items-center">
                    {course.is_free || course.price === 0 ? (
                      <span className="text-2xl font-bold text-green-600">FREE</span>
                    ) : (
                      <span className="text-2xl font-bold text-indigo-600">${course.price}</span>
                    )}
                    <button 
                      onClick={() => handleEnroll(course.id, course.is_free, course.price)}
                      disabled={enrolling === course.id}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                    >
                      {enrolling === course.id ? 'Enrolling...' : 'Enroll Now'}
                    </button>
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
