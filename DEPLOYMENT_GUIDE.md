# Deployment Guide: Task Manager Application

This guide explains how to deploy the frontend on Vercel and the backend on Hugging Face Spaces.

## Architecture Overview

- **Frontend**: Next.js 16+ application hosted on Vercel
- **Backend**: FastAPI application hosted on Hugging Face Spaces
- **Communication**: Frontend communicates with backend via REST API

## Backend Deployment (Hugging Face Spaces)

### Step 1: Prepare Repository
1. Create a new repository on Hugging Face containing the `backend/` folder
2. Ensure the following files are present:
   - `app.py` (with FastAPI app instance named `app`)
   - `requirements.txt` (with all dependencies)
   - `README.md` (deployment instructions)

### Step 2: Create Hugging Face Space
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select:
   - **Repository**: Your backend repository
   - **Space SDK**: Choose "Docker" for full control or "Gradio" if adapting to Gradio
   - **Hardware**: CPU (sufficient for most use cases)
   - **Visibility**: Public or Private as desired

### Step 3: Configure Environment Variables
In your Space settings, add the following environment variables:

```
DATABASE_URL=postgresql://username:password@hostname:port/database_name
SECRET_KEY=your-super-secret-jwt-key-change-this-to-a-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**Important Notes for Database on Hugging Face:**
- Hugging Face Spaces have ephemeral storage, so data doesn't persist between restarts
- Use an external PostgreSQL database (like Supabase, AWS RDS, or similar)
- For testing only, you can use SQLite but be aware of data loss on restarts

### Step 4: Monitor Deployment
- Check the Space logs to ensure successful deployment
- Note the Space URL (will be in the format `https://your-username-hf-space-name.hf.space`)

## Frontend Deployment (Vercel)

### Step 1: Prepare Repository
1. Create a new repository on GitHub containing the `frontend/` folder
2. Ensure the following files are present:
   - `package.json` with dependencies
   - `next.config.ts` or `next.config.js`
   - `vercel.json` (configuration file)
   - All Next.js app files

### Step 2: Deploy to Vercel
1. Go to [Vercel](https://vercel.com)
2. Sign in and click "New Project"
3. Import your frontend repository
4. During configuration:
   - **Framework Preset**: Next.js (should auto-detect)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next` (should auto-detect)
   - **Root Directory**: `.`

### Step 3: Configure Environment Variables
In your Vercel project settings, add the following environment variable:

```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-username.hf.space/api
```

**Note**: Replace `https://your-backend-username.hf.space/api` with your actual Hugging Face Space URL.

### Step 4: Deploy
1. Click "Deploy"
2. Wait for the build to complete
3. Your frontend will be available at a URL like `https://your-project-name.vercel.app`

## Post-Deployment Configuration

### Connecting Frontend and Backend
1. Once both deployments are successful, ensure the `NEXT_PUBLIC_API_BASE_URL` in your Vercel environment variables points to your Hugging Face Space URL
2. The URL should be in the format: `https://your-username-hf-space-name.hf.space/api`
3. Redeploy your frontend on Vercel if you changed the environment variable

## Testing the Deployment

1. Visit your Vercel frontend URL
2. Try registering a new user
3. Verify that authentication works
4. Create, update, and delete tasks to ensure full functionality
5. Check browser developer tools for any API errors

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your backend allows requests from your frontend domain
2. **Database Connection**: For Hugging Face Spaces, always use an external database
3. **Environment Variables**: Double-check that all variables are correctly set
4. **API URL Format**: Ensure the backend API is accessed at `/api/auth` and `/api/tasks`

### Backend Logs
- Check Hugging Face Space logs for any errors
- Look for database connection issues
- Verify the application starts successfully

### Frontend Logs
- Check Vercel deployment logs
- Use browser developer tools to inspect API requests
- Verify environment variables are correctly applied

## Scaling Considerations

### For Production Use
- Use a managed PostgreSQL database (Supabase, AWS RDS, Google Cloud SQL)
- Set up SSL certificates for secure connections
- Implement proper error logging and monitoring
- Consider rate limiting for API endpoints

### Performance
- Optimize database queries
- Implement caching where appropriate
- Use CDN for static assets
- Monitor response times and scale resources as needed

## Security Best Practices

1. Never expose sensitive keys in client-side code
2. Use HTTPS for all communications
3. Validate and sanitize all inputs
4. Keep dependencies updated
5. Use strong passwords and tokens
6. Implement proper authentication and authorization