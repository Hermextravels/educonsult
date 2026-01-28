'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState<string>('student');
  const [userName, setUserName] = useState<string>('');

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    const storedRole = localStorage.getItem('userRole');
    const storedName = localStorage.getItem('userName');
    
    setIsLoggedIn(!!token);
    if (storedRole) setUserRole(storedRole);
    if (storedName) setUserName(storedName);
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userName');
    setIsLoggedIn(false);
    router.push('/');
  };

  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-indigo-600">🎓</span>
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              EduConsult
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              href="/courses"
              className={`${
                pathname === '/courses'
                  ? 'text-indigo-600 font-semibold'
                  : 'text-gray-700 dark:text-gray-300 hover:text-indigo-600'
              }`}
            >
              Courses
            </Link>

            {isLoggedIn && (
              <>
                <Link
                  href="/dashboard"
                  className={`${
                    pathname === '/dashboard'
                      ? 'text-indigo-600 font-semibold'
                      : 'text-gray-700 dark:text-gray-300 hover:text-indigo-600'
                  }`}
                >
                  Dashboard
                </Link>

                {(userRole === 'instructor' || userRole === 'admin') && (
                  <Link
                    href="/admin"
                    className={`${
                      pathname?.startsWith('/admin')
                        ? 'text-indigo-600 font-semibold'
                        : 'text-gray-700 dark:text-gray-300 hover:text-indigo-600'
                    }`}
                  >
                    Admin
                  </Link>
                )}

                <Link
                  href="/profile"
                  className={`${
                    pathname === '/profile'
                      ? 'text-indigo-600 font-semibold'
                      : 'text-gray-700 dark:text-gray-300 hover:text-indigo-600'
                  }`}
                >
                  Profile
                </Link>
              </>
            )}
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <>
                <span className="text-sm text-gray-600 dark:text-gray-400 hidden md:block">
                  {userName}
                </span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-indigo-600"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}
