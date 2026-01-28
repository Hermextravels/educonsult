# EduLearn Platform - Full-Stack E-Learning Platform

A comprehensive full-stack e-learning platform built with Next.js (TypeScript) for the frontend and FastAPI (Python) for the backend.

## Features

### Core Features
- ✅ User registration, login, and profile management
- ✅ JWT-based authentication with role-based access control
- ✅ Course catalog with course creation and management
- ✅ Paid course enrollments and progress tracking
- ✅ Video and document-based lessons
- ✅ Quizzes with auto-grading (multiple choice and true/false)
- ✅ Automatic certificate generation upon course completion
- ✅ Student, instructor, and admin dashboards
- ✅ Paystack and Flutterwave payment integration with webhook verification
- ✅ Automatic enrollment after successful payment
- ✅ Revenue and enrollment reporting
- ✅ Admin course and user management tools

### Advanced Features
- 🔄 Background task processing with Celery
- 📧 Email notifications via SMTP
- 📊 Analytics and reporting
- 🔐 Secure password hashing with bcrypt
- 🌐 CORS support and API documentation
- 📱 Responsive design with Tailwind CSS
- 🗄️ PostgreSQL database with SQLAlchemy ORM

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Bcrypt
- **Task Queue**: Celery with Redis
- **PDF Generation**: ReportLab
- **API Documentation**: Swagger/OpenAPI

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios
- **UI Components**: Headless UI, Heroicons, Lucide React
- **Form Handling**: React Hook Form with Zod validation
- **Notifications**: React Hot Toast

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Payment Gateways**: Paystack, Flutterwave
- **Cloud Ready**: Designed for deployment on AWS, GCP, or Azure

## Project Structure

```
edulearn-platform/
├── backend/
│   ├── app/
│   │   ├── core/          # Configuration, database, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic
│   │   └── tasks/         # Celery tasks
│   ├── migrations/        # Alembic migrations
│   ├── main.py           # Application entry point
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js pages and routes
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities and API client
│   │   ├── hooks/        # Custom React hooks
│   │   ├── store/        # Zustand stores
│   │   ├── types/        # TypeScript types
│   │   └── styles/       # Global styles
│   ├── package.json
│   └── next.config.ts
├── docker-compose.yml    # Docker Compose configuration
└── README.md
```

## Installation & Setup

### Prerequisites
- Docker and Docker Compose
- OR Node.js 18+ and Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Quick Start with Docker

1. **Clone and setup environment**
```bash
cd edulearn-platform
cp backend/.env.example backend/.env
```

2. **Update configuration** in `backend/.env`:
```
DATABASE_URL=postgresql://user:password@postgres:5432/edulearn_db
SECRET_KEY=your-secure-secret-key-here
PAYSTACK_SECRET_KEY=your-paystack-key
FLUTTERWAVE_SECRET_KEY=your-flutterwave-key
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs

### Local Development

#### Backend Setup

1. **Create Python virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup database**
```bash
# Update DATABASE_URL in .env
export DATABASE_URL="postgresql://user:password@localhost:5432/edulearn_db"
alembic upgrade head
```

4. **Start Redis**
```bash
redis-server
```

5. **Start backend server**
```bash
uvicorn main:app --reload
```

6. **Start Celery worker** (in another terminal)
```bash
celery -A app.tasks.celery_app worker -l info
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.example .env.local
# Update NEXT_PUBLIC_API_URL if needed
```

3. **Start development server**
```bash
npm run dev
```

Access frontend at http://localhost:3000

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login user
- `POST /api/v1/users/refresh` - Refresh access token
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update user profile

### Courses
- `GET /api/v1/courses/` - List courses
- `POST /api/v1/courses/` - Create course (instructor)
- `GET /api/v1/courses/{id}` - Get course details
- `PUT /api/v1/courses/{id}` - Update course
- `DELETE /api/v1/courses/{id}` - Delete course

### Lessons
- `GET /api/v1/courses/{id}/lessons` - List lessons
- `POST /api/v1/courses/{id}/lessons` - Create lesson
- `PUT /api/v1/courses/{id}/lessons/{id}` - Update lesson

### Quizzes
- `GET /api/v1/quizzes/{id}` - Get quiz
- `POST /api/v1/quizzes/{course_id}/submit` - Submit quiz

### Payments
- `POST /api/v1/payments/initiate` - Initiate payment
- `POST /api/v1/payments/webhook/paystack` - Paystack webhook
- `POST /api/v1/payments/webhook/flutterwave` - Flutterwave webhook

### Certificates
- `POST /api/v1/certificates/generate/{id}` - Generate certificate
- `GET /api/v1/certificates/student/{id}` - Get certificate

### Dashboards
- `GET /api/v1/certificates/dashboard/student` - Student stats
- `GET /api/v1/certificates/dashboard/instructor` - Instructor stats
- `GET /api/v1/certificates/dashboard/admin` - Admin stats

## Role-Based Access Control

### Student
- Browse and enroll in courses
- View lessons and complete quizzes
- Download certificates
- Track progress

### Instructor
- Create and manage courses
- Add lessons and quizzes
- View student enrollments
- Track revenue

### Admin
- Manage all users
- Manage all courses
- View platform statistics
- Process refunds

## Payment Integration

### Paystack Integration
1. Get API keys from [Paystack Dashboard](https://dashboard.paystack.com)
2. Add `PAYSTACK_SECRET_KEY` to `.env`
3. Configure webhook URL in Paystack: `https://your-domain/api/v1/payments/webhook/paystack`

### Flutterwave Integration
1. Get API keys from [Flutterwave Dashboard](https://app.flutterwave.com)
2. Add `FLUTTERWAVE_SECRET_KEY` to `.env`
3. Configure webhook URL: `https://your-domain/api/v1/payments/webhook/flutterwave`

## Background Tasks

Tasks are processed asynchronously using Celery:

- **send_email** - Send email notifications
- **send_certificate_email** - Send certificate with PDF attachment
- **send_enrollment_notification** - Send enrollment confirmation
- **send_quiz_result_notification** - Send quiz results
- **generate_monthly_report** - Generate monthly reports

## Database Schema

### Core Tables
- `user` - User accounts with roles
- `course` - Course catalog
- `lesson` - Course lessons
- `quiz` - Quizzes for assessment
- `question` - Quiz questions
- `answer` - Quiz answer options
- `course_enrollment` - Student enrollments
- `quiz_attempt` - Quiz submissions
- `payment` - Payment records
- `certificate` - Issued certificates
- `notification` - User notifications

## Deployment

### Environment Variables

Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/db

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Payment
PAYSTACK_SECRET_KEY=your-key
FLUTTERWAVE_SECRET_KEY=your-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend frontend
```

### Cloud Deployment (AWS/GCP/Azure)

The platform is designed to be cloud-ready:
- Database: Use managed RDS/Cloud SQL/Azure Database
- Cache: Use ElastiCache/Memorystore/Azure Cache
- Storage: Use S3/GCS/Azure Blob for files
- Email: Use SES/SendGrid/Azure Communication Services

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Future Enhancements

- [ ] Live video streaming with WebRTC
- [ ] Advanced analytics and learning paths
- [ ] Academic journal submissions
- [ ] Third-party API integrations
- [ ] Mobile app (React Native)
- [ ] AI-powered recommendations
- [ ] Real-time collaboration tools
- [ ] Advanced payment options (Stripe, Apple Pay)

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For support, email support@edulearn.com or create an issue in the repository.

---

**Built with ❤️ for learners and educators worldwide**
