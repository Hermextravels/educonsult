export type UserRole = 'student' | 'instructor' | 'admin'

export interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: UserRole
  is_active: boolean
  is_verified: boolean
  avatar_url?: string
  bio?: string
  phone?: string
  created_at: string
}

export interface Course {
  id: number
  title: string
  description: string
  slug: string
  thumbnail_url?: string
  price: number
  currency: string
  duration_weeks?: number
  level: string
  category: string
  is_published: boolean
  instructor_id: number
  students_count?: number
  created_at: string
  updated_at: string
}

export interface Lesson {
  id: number
  course_id: number
  title: string
  description?: string
  order: number
  content_type: string
  content_url: string
  duration_minutes?: number
  is_published: boolean
  created_at: string
}

export interface Quiz {
  id: number
  course_id: number
  title: string
  description?: string
  passing_score: number
  time_limit_minutes?: number
  is_published: boolean
  question_count: number
  created_at: string
}

export interface Question {
  id: number
  quiz_id: number
  question_text: string
  question_type: string
  order: number
}

export interface QuizAttempt {
  id: number
  quiz_id: number
  user_id: number
  score?: number
  passed?: boolean
  started_at: string
  completed_at?: string
}

export interface Payment {
  id: number
  user_id: number
  course_id: number
  amount: number
  currency: string
  payment_method: string
  status: string
  transaction_id: string
  reference: string
  created_at: string
}

export interface Certificate {
  id: number
  user_id: number
  course_id: number
  certificate_number: string
  issue_date: string
  pdf_url: string
}

export interface Enrollment {
  user_id: number
  course_id: number
  enrolled_at: string
  progress: number
}

export interface DashboardStats {
  total_courses_enrolled?: number
  completed_courses?: number
  in_progress_courses?: number
  total_certificates?: number
  average_grade?: number
  total_courses?: number
  total_students?: number
  total_revenue?: number
  total_users?: number
}
