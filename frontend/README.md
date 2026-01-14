# Task Manager Frontend

This is the frontend for the Task Manager application, built with Next.js 16+.

## Deployment

This application is designed to be deployed on Vercel.

### Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend API (e.g., `https://your-backend.hf.space/api`)

### Local Development

```bash
npm install
npm run dev
```

### Build for Production

```bash
npm run build
```

## Deployment Instructions

1. Fork this repository
2. Go to [Vercel](https://vercel.com) and sign in
3. Click "New Project" and import your forked repository
4. During the configuration:
   - Framework preset: Next.js
   - Build command: `npm run build`
   - Output directory: `.next`
   - Environment variables: Add your `NEXT_PUBLIC_API_BASE_URL`
5. Click "Deploy"

Your application will be deployed and available at a URL like `https://your-app.vercel.app`.

## Configuration

The frontend expects the backend API to be available at the URL specified in the `NEXT_PUBLIC_API_BASE_URL` environment variable, with endpoints at `/api/auth` and `/api/tasks`.


# // fix.