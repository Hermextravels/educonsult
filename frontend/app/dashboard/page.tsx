'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);

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

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-xl text-gray-600 dark:text-gray-300">Loading...</div>
      </div>
    );
  }

  return (
    <div className="bg-slate-50 dark:bg-gray-900">
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/10 via-sky-500/10 to-purple-500/10" />
        <div className="relative max-w-7xl mx-auto px-4 pt-10 pb-8 sm:pt-14 sm:pb-10">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-semibold text-indigo-600 dark:text-indigo-300">Dashboard</p>
              <h2 className="mt-2 text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
                Welcome back, {user?.full_name || user?.username || 'Learner'}
              </h2>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                Role: <span className="font-semibold capitalize">{user?.role || 'student'}</span>
                <span className="mx-2 text-gray-400">•</span>
                Email: <span className="font-semibold">{user?.email || '—'}</span>
              </p>
            </div>
            <div className="flex gap-3">
              <Link
                href="/courses"
                className="inline-flex items-center justify-center rounded-lg border border-indigo-200 dark:border-indigo-800 px-4 py-2 text-sm font-semibold text-indigo-700 dark:text-indigo-200 hover:bg-indigo-50 dark:hover:bg-indigo-900/30"
              >
                Browse Courses
              </Link>
              <button
                onClick={handleLogout}
                className="inline-flex items-center justify-center rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 pb-12">
        <div className="grid gap-6 md:grid-cols-3">
          <div className="group rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-sm ring-1 ring-gray-200/70 dark:ring-gray-700/70">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">My Courses</p>
                <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">0</p>
              </div>
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100 text-2xl text-indigo-600 dark:bg-indigo-900/40 dark:text-indigo-300">
                📚
              </span>
            </div>
            <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">Start learning with curated expert-led courses.</p>
          </div>

          <div className="group rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-sm ring-1 ring-gray-200/70 dark:ring-gray-700/70">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Completed</p>
                <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">0</p>
              </div>
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-2xl text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-300">
                ✅
              </span>
            </div>
            <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">Track your progress and celebrate milestones.</p>
          </div>

          <div className="group rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-sm ring-1 ring-gray-200/70 dark:ring-gray-700/70">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Certificates</p>
                <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">0</p>
              </div>
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 text-2xl text-amber-600 dark:bg-amber-900/40 dark:text-amber-300">
                🏆
              </span>
            </div>
            <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">Earn certificates to showcase your skills.</p>
          </div>
        </div>

        <div className="mt-10 rounded-2xl bg-white dark:bg-gray-800 p-6 sm:p-8 shadow-sm ring-1 ring-gray-200/70 dark:ring-gray-700/70">
          <div className="flex items-center justify-between">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">Quick Actions</h3>
            <Link href="/profile" className="text-sm font-semibold text-indigo-600 dark:text-indigo-300">
              View Profile
            </Link>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <Link
              href="/courses"
              className="group flex items-start gap-4 rounded-xl border border-indigo-100 dark:border-indigo-900/60 bg-indigo-50/40 dark:bg-indigo-900/20 p-5 transition hover:translate-y-0.5"
            >
              <span className="text-2xl">🔍</span>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Browse Courses</h4>
                <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">Explore available courses and enroll in minutes.</p>
              </div>
            </Link>

            <Link
              href="/profile"
              className="group flex items-start gap-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white/70 dark:bg-gray-900/40 p-5 transition hover:translate-y-0.5"
            >
              <span className="text-2xl">👤</span>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Update Profile</h4>
                <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">Personalize your profile and preferences.</p>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
