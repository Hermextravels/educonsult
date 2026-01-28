'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/auth'
import { useAuth } from '@/hooks/useAuth'
import { apiClient } from '@/lib/api-client'
import { DashboardStats } from '@/types'
import Link from 'next/link'

export default function Dashboard() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuthStore()
  const { logout } = useAuth()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    fetchDashboardData()
  }, [isAuthenticated, router, user])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      if (user?.role === 'student') {
        const response = await apiClient.getStudentDashboard()
        setStats(response.data)
      } else if (user?.role === 'instructor') {
        const response = await apiClient.getInstructorDashboard()
        setStats(response.data)
      } else if (user?.role === 'admin') {
        const response = await apiClient.getAdminDashboard()
        setStats(response.data)
      }
    } catch (error) {
      console.error('Failed to fetch dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">EduLearn Dashboard</h1>
          <div className="flex gap-4 items-center">
            <span className="text-gray-600">Welcome, {user.full_name}</span>
            <button onClick={logout} className="btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="container py-12">
        {/* User Role Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-6">
            {user.role === 'student' && "Student Dashboard"}
            {user.role === 'instructor' && "Instructor Dashboard"}
            {user.role === 'admin' && "Admin Dashboard"}
          </h2>

          {/* Stats Grid */}
          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-600">Loading dashboard...</p>
            </div>
          ) : stats ? (
            <>
              <div className="grid md:grid-cols-4 gap-4 mb-8">
                {user.role === 'student' && (
                  <>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Enrolled Courses</p>
                      <p className="text-4xl font-bold text-primary">
                        {stats.total_courses_enrolled || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Completed</p>
                      <p className="text-4xl font-bold text-green-600">
                        {stats.completed_courses || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">In Progress</p>
                      <p className="text-4xl font-bold text-yellow-600">
                        {stats.in_progress_courses || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Certificates</p>
                      <p className="text-4xl font-bold text-blue-600">
                        {stats.total_certificates || 0}
                      </p>
                    </div>
                  </>
                )}
                {user.role === 'instructor' && (
                  <>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Total Courses</p>
                      <p className="text-4xl font-bold text-primary">
                        {stats.total_courses || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Total Students</p>
                      <p className="text-4xl font-bold text-blue-600">
                        {stats.total_students || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Revenue</p>
                      <p className="text-4xl font-bold text-green-600">
                        ${stats.total_revenue || 0}
                      </p>
                    </div>
                  </>
                )}
                {user.role === 'admin' && (
                  <>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Total Users</p>
                      <p className="text-4xl font-bold text-primary">
                        {stats.total_users || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Total Courses</p>
                      <p className="text-4xl font-bold text-blue-600">
                        {stats.total_courses || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Revenue</p>
                      <p className="text-4xl font-bold text-green-600">
                        ${stats.total_revenue || 0}
                      </p>
                    </div>
                    <div className="card">
                      <p className="text-gray-600 text-sm">Pending Payments</p>
                      <p className="text-4xl font-bold text-orange-600">
                        {stats.pending_payments || 0}
                      </p>
                    </div>
                  </>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4">
                {user.role === 'student' && (
                  <Link href="/courses" className="btn-primary">
                    Browse Courses
                  </Link>
                )}
                {user.role === 'instructor' && (
                  <Link href="/instructor/courses" className="btn-primary">
                    Manage Courses
                  </Link>
                )}
                {user.role === 'admin' && (
                  <Link href="/admin/users" className="btn-primary">
                    Manage Users
                  </Link>
                )}
                <Link href="/profile" className="btn-secondary">
                  View Profile
                </Link>
              </div>
            </>
          ) : null}
        </div>
      </main>
    </div>
  )
}
