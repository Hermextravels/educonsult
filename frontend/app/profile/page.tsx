'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface UserProfile {
  id: number;
  email: string;
  username: string;
  full_name?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  role: string;
  bio?: string | null;
  phone?: string | null;
  avatar_url?: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<UserProfile | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      router.push('/login');
      return;
    }

    const fetchMe = async (accessToken: string) => {
      return fetch('http://localhost:8000/api/v1/users/me', {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
    };

    const refreshAccessToken = async () => {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        return null;
      }

      const response = await fetch('http://localhost:8000/api/v1/users/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
      });

      if (!response.ok) {
        return null;
      }

      const data = await response.json();
      if (data?.access_token) {
        localStorage.setItem('accessToken', data.access_token);
      }
      if (data?.refresh_token) {
        localStorage.setItem('refreshToken', data.refresh_token);
      }

      return data?.access_token || null;
    };

    const loadUser = async () => {
      try {
        let response = await fetchMe(token);

        if (response.status === 401) {
          const newAccessToken = await refreshAccessToken();
          if (newAccessToken) {
            response = await fetchMe(newAccessToken);
          }
        }

        if (!response.ok) {
          throw new Error('Unauthorized');
        }

        const data = await response.json();
        setUser(data);
        setLoading(false);
      } catch {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        router.push('/login');
      }
    };

    loadUser();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-xl text-gray-600 dark:text-gray-300">Loading...</div>
      </div>
    );
  }

  const displayName = user?.full_name || [user?.first_name, user?.last_name].filter(Boolean).join(' ') || user?.username;

  return (
    <div className="bg-slate-50 dark:bg-gray-900">
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold text-indigo-600 dark:text-indigo-300">Profile</p>
            <h1 className="mt-2 text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
              {displayName || 'Your Profile'}
            </h1>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Keep your details up to date for a personalized learning experience.
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              href="/dashboard"
              className="inline-flex items-center justify-center rounded-lg border border-gray-200 dark:border-gray-700 px-4 py-2 text-sm font-semibold text-gray-700 dark:text-gray-200 hover:bg-white/60 dark:hover:bg-gray-800"
            >
              Back to Dashboard
            </Link>
            <Link
              href="/courses"
              className="inline-flex items-center justify-center rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
            >
              Browse Courses
            </Link>
          </div>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2 rounded-2xl bg-white dark:bg-gray-800 p-6 sm:p-8 shadow-sm ring-1 ring-gray-200/70 dark:ring-gray-700/70">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Account Details</h2>
            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Full Name</p>
                <p className="mt-1 text-base font-semibold text-gray-900 dark:text-white">
                  {displayName || '—'}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Role</p>
                <p className="mt-1 inline-flex items-center rounded-full bg-indigo-50 px-3 py-1 text-sm font-semibold text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-200">
                  {user?.role || 'student'}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Email</p>
                <p className="mt-1 text-base font-semibold text-gray-900 dark:text-white">
                  {user?.email || '—'}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Username</p>
                <p className="mt-1 text-base font-semibold text-gray-900 dark:text-white">
                  {user?.username || '—'}
                </p>
              </div>
            </div>

            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Phone</p>
                <p className="mt-1 text-base font-semibold text-gray-900 dark:text-white">
                  {user?.phone || 'Not provided'}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Member Since</p>
                <p className="mt-1 text-base font-semibold text-gray-900 dark:text-white">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
                </p>
              </div>
            </div>

            <div className="mt-8">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Bio</p>
              <p className="mt-2 text-gray-700 dark:text-gray-300">
                {user?.bio || 'Add a short bio to tell others about your learning goals.'}
              </p>
            </div>
          </div>

          <div className="rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-sm ring-1 ring-gray-200/70 dark:ring-gray-700/70">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Quick Links</h3>
            <div className="mt-4 space-y-3">
              <Link
                href="/dashboard"
                className="flex items-center justify-between rounded-lg border border-gray-200 dark:border-gray-700 px-4 py-3 text-sm font-semibold text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-900/40"
              >
                Dashboard
                <span>→</span>
              </Link>
              <Link
                href="/courses"
                className="flex items-center justify-between rounded-lg border border-indigo-100 dark:border-indigo-900/70 bg-indigo-50/50 dark:bg-indigo-900/30 px-4 py-3 text-sm font-semibold text-indigo-700 dark:text-indigo-200 hover:bg-indigo-50"
              >
                Explore Courses
                <span>→</span>
              </Link>
              <div className="rounded-lg border border-gray-200 dark:border-gray-700 px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                Edit profile and preferences will be available soon.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
