# Deployment Guide for EduConsult Learning Platform

## ✅ Git Repository Initialized

Your code is ready to push! Here's how to deploy:

## Step 1: Create GitHub Repository

### Option A: Using GitHub Website (Recommended)
1. Go to https://github.com/new
2. Repository name: `edulearn-platform` (or your preferred name)
3. Description: "EduConsult Learning Platform - Full-stack learning management system"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have them)
6. Click "Create repository"

### Option B: Install GitHub CLI (Optional)
```bash
brew install gh
gh auth login
gh repo create edulearn-platform --public --source=. --remote=origin --push
```

## Step 2: Push Your Code

After creating the repository on GitHub, copy the commands shown and run:

```bash
cd /Users/mac/Desktop/educonsoult/edulearn-platform

# Add the remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/edulearn-platform.git

# Push your code
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Production

### Option 1: Deploy to Railway (Easiest)

**Backend:**
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `edulearn-platform` repository
5. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://... (Railway will provide)
   ```

**Frontend:**
1. Create another service for frontend
2. Configure:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Start Command: `npm start`
3. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```

### Option 2: Deploy to Vercel + Heroku

**Backend (Heroku):**
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login and create app
heroku login
cd backend
heroku create your-app-name-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git subtree push --prefix backend heroku main
```

**Frontend (Vercel):**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

### Option 3: Deploy to DigitalOcean App Platform

1. Go to https://cloud.digitalocean.com/apps
2. Create App → From GitHub
3. Select your repository
4. Add two components:
   - **Backend**: Root Directory `backend`, Run Command: `uvicorn main:app --host 0.0.0.0 --port 8080`
   - **Frontend**: Root Directory `frontend`, Build: `npm run build`, Run: `npm start`

### Option 4: Docker Deployment (Any VPS)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build separately
docker build -t edulearn-backend ./backend
docker build -t edulearn-frontend ./frontend

docker run -d -p 8000:8000 edulearn-backend
docker run -d -p 3000:3000 edulearn-frontend
```

## Environment Variables Needed

### Backend (.env)
```env
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=postgresql://user:password@localhost/edulearn
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://localhost:6379
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
# Or in production:
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## Post-Deployment Setup

1. **Seed Admin User:**
   ```bash
   # SSH into your backend server or run locally against production DB
   python seed_admin.py
   ```
   
   Default admin credentials:
   - Email: admin@educonsult.com
   - Password: Admin@12345

2. **Create Tables:**
   Tables will be created automatically on first run via SQLAlchemy

3. **Update API URLs:**
   Update all `http://localhost:8000` references in frontend to your production backend URL

## Current Project Status

✅ **Completed Features:**
- User authentication (JWT-based)
- Role-based access control (Admin, Instructor, Student)
- Course management (CRUD operations)
- Course enrollment system
- File upload system (videos, thumbnails, materials)
- Admin dashboard
- User management
- Course visibility controls
- Free vs paid course distinction

🔄 **Pending Features:**
- Payment integration (Stripe/PayPal)
- Quiz system (backend ready, needs frontend)
- Certificate generation
- Video streaming optimization
- Email notifications
- Course progress tracking
- Discussion forums

## Repository Structure
```
edulearn-platform/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── main.py
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── app/
│   ├── components/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Quick Commands Reference

```bash
# Start development servers
cd backend && uvicorn main:app --reload --port 8000
cd frontend && npm run dev

# Seed admin user
cd backend && python seed_admin.py

# Run with Docker
docker-compose up -d

# Push to GitHub
git add .
git commit -m "Your commit message"
git push origin main
```

## Support & Documentation

- Full API Documentation: See `API_DOCUMENTATION.md`
- Setup Guide: See `SETUP_GUIDE.md`
- Architecture: See `ARCHITECTURE.md`
- File Upload Guide: See `FILE_UPLOAD_FEATURE.md`

---

**Ready to deploy!** 🚀 Follow the steps above to get your platform live.
