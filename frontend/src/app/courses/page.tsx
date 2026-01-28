'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/auth'
import { apiClient } from '@/lib/api-client'
import { Course } from '@/types'
import Link from 'next/link'

export default function Courses() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState<string>('')

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    fetchCourses()
  }, [isAuthenticated, router, category])

  const fetchCourses = async () => {
    try {
      setLoading(true)
      const response = await apiClient.getCourses(0, 20, category || undefined)
      setCourses(response.data)
    } catch (error) {
      console.error('Failed to fetch courses:', error)
    } finally {
      setLoading(false)
    }
  }

  const categories = ['Web Development', 'Data Science', 'Mobile Development', 'Cloud Computing']

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container py-4 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-primary">
            EduLearn
          </Link>
          <button
            onClick={() => router.push('/dashboard')}
            className="text-gray-600 hover:text-gray-900"
          >
            Dashboard
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-12">
        <h1 className="text-4xl font-bold mb-2">Explore Courses</h1>
        <p className="text-gray-600 mb-8">Find and enroll in courses that match your interests</p>

        {/* Category Filter */}
        <div className="mb-8 flex gap-2 flex-wrap">
          <button
            onClick={() => setCategory('')}
            className={`px-4 py-2 rounded-lg font-semibold ${
              category === '' ? 'btn-primary' : 'btn-secondary'
            }`}
          >
            All
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-lg font-semibold ${
                category === cat ? 'btn-primary' : 'btn-secondary'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Courses Grid */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Loading courses...</p>
          </div>
        ) : courses.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">No courses found. Check back later!</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-6">
            {courses.map((course) => (
              <Link
                key={course.id}
                href={`/courses/${course.id}`}
                className="card group cursor-pointer"
              >
                {course.thumbnail_url && (
                  <div className="h-48 bg-gray-200 rounded-lg mb-4 overflow-hidden">
                    <img
                      src={course.thumbnail_url}
                      alt={course.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                    />
                  </div>
                )}
                <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">
                  {course.title}
                </h3>
                <p className="text-gray-600 mb-4 line-clamp-2">{course.description}</p>
                <div className="flex justify-between items-center">
                  <span className="text-lg font-bold text-primary">
                    {course.price === 0 ? 'Free' : `$${course.price}`}
                  </span>
                  <span className="text-sm text-gray-500">{course.students_count || 0} students</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
