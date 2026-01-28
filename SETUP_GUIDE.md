# EduLearn Platform - Setup & Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Docker Quick Start](#docker-quick-start)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Backend Configuration](#backend-configuration)
6. [Frontend Configuration](#frontend-configuration)
7. [Payment Gateway Setup](#payment-gateway-setup)
8. [Email Configuration](#email-configuration)
9. [Production Deployment](#production-deployment)
10. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Git

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd edulearn-platform
```

### Step 2: Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create environment file**
```bash
cp .env.example .env
```

4. **Update .env with your configuration**
```
DATABASE_URL=postgresql://user:password@localhost:5432/edulearn_db
SECRET_KEY=your-very-secure-secret-key-minimum-32-chars
PAYSTACK_SECRET_KEY=your-paystack-key
FLUTTERWAVE_SECRET_KEY=your-flutterwave-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

5. **Create PostgreSQL database**
```bash
createdb edulearn_db -U postgres
```

6. **Run migrations**
```bash
alembic upgrade head
```

7. **Start Redis** (in another terminal)
```bash
redis-server
```

8. **Start Celery worker** (in another terminal)
```bash
celery -A app.tasks.celery_app worker -l info
```

9. **Start FastAPI server** (in another terminal)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Frontend Setup

1. **Install dependencies**
```bash
cd ../frontend
npm install
```

2. **Create environment file**
```bash
cp .env.example .env.local
```

3. **Start development server**
```bash
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

## Docker Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Step 1: Configuration
```bash
# Copy environment file
cp backend/.env.example backend/.env

# Edit backend/.env with your credentials
nano backend/.env
```

### Step 2: Build and Start
```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 3: Initialize Database
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create admin user (optional)
docker-compose exec backend python -c "
from app.models.models import User
from app.core.database import SessionLocal
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email='admin@example.com',
    username='admin',
    full_name='Admin User',
    hashed_password=get_password_hash('admin123'),
    role='admin',
    is_active=True,
    is_verified=True
)
db.add(admin)
db.commit()
print('Admin user created')
"
```

### Step 4: Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- PgAdmin: http://localhost:5050 (optional)

## Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/edulearn_db

# JWT Configuration
SECRET_KEY=your-secret-key-min-32-chars-very-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=EduLearn Platform
DEBUG=False  # Set to False in production

# Payment Gateways
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxx
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-xxxxxxxxxxxxx

# Email Configuration
EMAIL_FROM=noreply@edulearn.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# File Upload
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_VIDEO_EXTENSIONS=.mp4,.avi,.mov,.mkv
ALLOWED_DOC_EXTENSIONS=.pdf,.docx,.pptx,.txt

# AWS (Optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Database Setup

### PostgreSQL

1. **Install PostgreSQL** (if not already installed)
```bash
# macOS
brew install postgresql@15

# Ubuntu
sudo apt-get install postgresql postgresql-contrib

# Windows: Download installer from postgresql.org
```

2. **Start PostgreSQL service**
```bash
# macOS
brew services start postgresql@15

# Ubuntu
sudo systemctl start postgresql

# Windows
# Use Services app or pgAdmin
```

3. **Create database and user**
```bash
psql postgres

postgres=# CREATE USER edulearn WITH PASSWORD 'password';
postgres=# CREATE DATABASE edulearn_db OWNER edulearn;
postgres=# ALTER ROLE edulearn SET client_encoding TO 'utf8';
postgres=# ALTER ROLE edulearn SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE edulearn SET default_transaction_deferrable TO on;
postgres=# GRANT ALL PRIVILEGES ON DATABASE edulearn_db TO edulearn;
postgres=# \q
```

4. **Verify connection**
```bash
psql -U edulearn -d edulearn_db -h localhost
```

## Backend Configuration

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Revert migrations:
```bash
alembic downgrade -1
```

### Celery Configuration

Start worker:
```bash
celery -A app.tasks.celery_app worker -l info
```

Start beat scheduler (for periodic tasks):
```bash
celery -A app.tasks.celery_app beat -l info
```

Monitor tasks:
```bash
celery -A app.tasks.celery_app events
```

## Frontend Configuration

### Build for Production

```bash
npm run build
npm start
```

### Environment Variables

Key environment variables:
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NODE_ENV` - Set to 'production' for production builds

## Payment Gateway Setup

### Paystack Integration

1. **Create account** at https://paystack.com
2. **Get API keys** from Dashboard → Settings → API Keys
3. **Add to .env**
```env
PAYSTACK_SECRET_KEY=sk_test_xxxxx
```

4. **Configure webhook**
- URL: `https://your-domain.com/api/v1/payments/webhook/paystack`
- Events: charge.success, charge.failed

### Flutterwave Integration

1. **Create account** at https://flutterwave.com
2. **Get API keys** from Settings → API Keys
3. **Add to .env**
```env
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-xxxxx
```

4. **Configure webhook**
- URL: `https://your-domain.com/api/v1/payments/webhook/flutterwave`
- Events: charge.completed, charge.failed

## Email Configuration

### Gmail Setup (Recommended for Development)

1. **Enable 2-Factor Authentication** in Gmail
2. **Generate App Password**
   - Go to myaccount.google.com/apppasswords
   - Select Mail and Windows Device
   - Copy the 16-character password

3. **Add to .env**
```env
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

### SendGrid Setup (For Production)

1. **Create account** at https://sendgrid.com
2. **Create API key** in Settings → API Keys
3. **Update backend** to use SendGrid client

### AWS SES Setup (For Production)

1. **Configure AWS SES** in your AWS account
2. **Get credentials** from IAM
3. **Update backend** to use boto3 for SES

## Production Deployment

### AWS Deployment

1. **RDS PostgreSQL**
```bash
# Create RDS instance via AWS Console
# Note the endpoint and credentials
```

2. **ElastiCache Redis**
```bash
# Create Redis cluster for Celery
```

3. **EC2 Instance**
```bash
# Launch Ubuntu 22.04 LTS instance
# Security group: Allow ports 80, 443, 8000
```

4. **SSH into instance**
```bash
ssh -i key.pem ubuntu@your-instance-ip
```

5. **Install dependencies**
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev
sudo apt-get install nodejs npm
sudo apt-get install nginx supervisor
```

6. **Clone and setup**
```bash
git clone <repo>
cd edulearn-platform/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

7. **Configure environment**
```bash
nano .env
# Add production values
```

8. **Setup Nginx reverse proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }
}
```

9. **Setup SSL with Let's Encrypt**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Docker Deployment

1. **Push to Docker Hub**
```bash
docker login
docker tag edulearn-backend:latest your-username/edulearn-backend:latest
docker push your-username/edulearn-backend:latest
```

2. **Deploy on any Docker host**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Database Backup

```bash
# Backup
pg_dump edulearn_db > backup.sql

# Restore
psql edulearn_db < backup.sql
```

## Troubleshooting

### Backend Issues

**Port already in use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Use different port
uvicorn main:app --port 8001
```

**Database connection error**
```bash
# Check PostgreSQL is running
psql -U edulearn -d edulearn_db

# Check connection string in .env
echo $DATABASE_URL
```

**Celery worker not processing tasks**
```bash
# Start Redis
redis-server

# Check Celery logs
celery -A app.tasks.celery_app worker -l debug
```

### Frontend Issues

**API connection refused**
```bash
# Check backend is running
curl http://localhost:8000/health

# Check NEXT_PUBLIC_API_URL in .env.local
cat .env.local
```

**Port 3000 already in use**
```bash
# Use different port
npm run dev -- -p 3001
```

### General Issues

**Clear all cache**
```bash
# Backend
rm -rf __pycache__ .pytest_cache

# Frontend
rm -rf .next node_modules
npm install
```

**Reset database**
```bash
# Backup first!
pg_dump edulearn_db > backup.sql

# Drop and recreate
dropdb edulearn_db
createdb edulearn_db -U edulearn
alembic upgrade head
```

---

For more help, check the main README.md or open an issue on GitHub.
