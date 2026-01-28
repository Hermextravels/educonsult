'use client';

import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <div className="mx-auto max-w-6xl px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome to EduConsult Platform
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Transform your learning journey with expert guidance and consultation
          </p>
          <Link href="/register" className="inline-block bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700 text-lg font-semibold">
            Get Started Now
          </Link>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
            <div className="text-4xl mb-4">📚</div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Diverse Courses</h3>
            <p className="text-gray-600 dark:text-gray-300">Access hundreds of courses in various subjects and skill levels</p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Learn at Your Pace</h3>
            <p className="text-gray-600 dark:text-gray-300">Study whenever and wherever you want with lifetime access</p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
            <div className="text-4xl mb-4">🏆</div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Earn Certificates</h3>
            <p className="text-gray-600 dark:text-gray-300">Complete courses and earn recognized certificates</p>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 bg-indigo-600 text-white p-12 rounded-lg text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to start learning?</h3>
          <p className="text-lg mb-6">Join thousands of students advancing their careers</p>
          <Link href="/register" className="inline-block bg-white text-indigo-600 px-8 py-3 rounded-lg hover:bg-gray-100 font-semibold">
            Sign Up Free
          </Link>
        </div>
      </div>
    </div>
  );
}
