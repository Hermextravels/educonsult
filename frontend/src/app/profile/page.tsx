'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/auth'
import { useAuth } from '@/hooks/useAuth'
import Link from 'next/link'

export default function Profile() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuthStore()
  const { updateProfile, logout } = useAuth()
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    phone: user?.phone || '',
    bio: user?.bio || '',
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    await updateProfile(formData)
    setEditing(false)
    setLoading(false)
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container py-4 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-primary">
            EduLearn
          </Link>
          <button onClick={logout} className="btn-secondary">
            Logout
          </button>
        </div>
      </header>

      <main className="container py-12">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">My Profile</h1>

          <div className="card">
            {!editing ? (
              <div>
                <div className="mb-6">
                  <h2 className="text-2xl font-bold mb-4">{user.full_name}</h2>
                  <p className="text-gray-600 mb-2">
                    <strong>Email:</strong> {user.email}
                  </p>
                  <p className="text-gray-600 mb-2">
                    <strong>Username:</strong> {user.username}
                  </p>
                  <p className="text-gray-600 mb-2">
                    <strong>Role:</strong> {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                  </p>
                  {user.phone && (
                    <p className="text-gray-600 mb-2">
                      <strong>Phone:</strong> {user.phone}
                    </p>
                  )}
                  {user.bio && (
                    <p className="text-gray-600 mb-2">
                      <strong>Bio:</strong> {user.bio}
                    </p>
                  )}
                  <p className="text-gray-600 text-sm">
                    <strong>Member since:</strong> {new Date(user.created_at).toLocaleDateString()}
                  </p>
                </div>
                <button onClick={() => setEditing(true)} className="btn-primary">
                  Edit Profile
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="label">Full Name</label>
                  <input
                    type="text"
                    name="full_name"
                    className="input"
                    value={formData.full_name}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div>
                  <label className="label">Phone</label>
                  <input
                    type="tel"
                    name="phone"
                    className="input"
                    value={formData.phone}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label className="label">Bio</label>
                  <textarea
                    name="bio"
                    className="input resize-none h-24"
                    value={formData.bio}
                    onChange={handleChange}
                  />
                </div>

                <div className="flex gap-2">
                  <button type="submit" className="btn-primary" disabled={loading}>
                    {loading ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setEditing(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
