# How to Deploy Frontend to Vercel

## Step 1: Connect GitHub to Vercel

1. Go to **https://vercel.com**
2. Click **Sign Up** (or Sign In if you have an account)
3. Choose **Continue with GitHub**
4. Authorize Vercel to access your GitHub account

## Step 2: Import Your Repository

1. After signing in, click **Add New** → **Project**
2. Click **Import Git Repository**
3. Paste your repo URL: `https://github.com/Hermextravels/educonsult.git`
4. Click **Continue**

## Step 3: Configure the Project

On the "Import Project" page:

### **Root Directory:**
Change from `./` to `./frontend` (because your Next.js app is in the frontend folder)

### **Environment Variables:**
Click **Add Environment Variable** and add:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `https://educonsult-tj33.onrender.com/api/v1` |

### **Build & Development Settings:**
These should auto-detect as correct:
- **Framework Preset:** Next.js
- **Build Command:** `npm run build` (auto-detected)
- **Output Directory:** `.next` (auto-detected)
- **Install Command:** `npm install` (auto-detected)

## Step 4: Deploy

1. Click **Deploy**
2. Wait ~2-3 minutes for the build to complete
3. You'll see a **Production URL** like: `https://educonsult.vercel.app`

## Step 5: Test Your Deployment

1. Visit your new URL
2. Try to **Login** with:
   - Email: `admin@educonsult.com`
   - Password: `Admin@12345`
3. Try to **Enroll** in a course

If you see errors, check the browser console (F12) for error messages.

---

## ⚡ Quick Troubleshooting

### Error: "Failed to fetch from API"
- Make sure `NEXT_PUBLIC_API_URL` is set correctly
- Check that your Render backend is running: https://educonsult-tj33.onrender.com/docs

### Error: "CORS error"
- This means the frontend and backend URLs don't match
- Update the backend CORS settings to include your Vercel URL

### Build failed
- Check the build logs in Vercel dashboard
- Usually due to TypeScript errors or missing dependencies

---

## 📝 After Deployment

**If you need to update environment variables later:**
1. Go to your Vercel project dashboard
2. Click **Settings** → **Environment Variables**
3. Edit the `NEXT_PUBLIC_API_URL` 
4. Redeploy (Vercel will auto-redeploy on git push)

---

## 🎯 Current Status After Deploy

| Component | Status | URL |
|-----------|--------|-----|
| Backend | ✅ Live | https://educonsult-tj33.onrender.com |
| Frontend | ⏳ Deploying | https://educonsult.vercel.app (after deploy) |
| GitHub Repo | ✅ Live | https://github.com/Hermextravels/educonsult |

---

## 💡 Pro Tips

- **Auto-redeploy**: Every time you `git push` to main, Vercel auto-deploys
- **Preview URLs**: Each pull request gets a preview deployment
- **Logs**: Check Vercel dashboard → Deployments → Logs for debugging
- **Speed**: Vercel uses edge network for super fast loading worldwide

Done! Your app will be live in minutes! 🚀
