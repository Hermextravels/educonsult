import type { Metadata } from 'next'
import { Toaster } from 'react-hot-toast'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'EduLearn - Your Learning Platform',
  description: 'Access high-quality courses from expert instructors',
  openGraph: {
    title: 'EduLearn - Your Learning Platform',
    description: 'Access high-quality courses from expert instructors',
    url: 'https://edulearn.com',
    siteName: 'EduLearn',
    locale: 'en_US',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#1a5490" />
      </head>
      <body className="antialiased">
        {children}
        <Toaster position="top-right" />
      </body>
    </html>
  )
}
