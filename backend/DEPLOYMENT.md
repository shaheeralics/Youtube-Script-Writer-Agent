# Deployment Guide

## Quick Deployment Options

### 1. Railway (Recommended - Free Tier Available)

1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your YouTube Script Writer repository
5. Choose the `backend` folder as the root directory
6. Railway will auto-detect Python and deploy
7. Add environment variable: `OPENAI_API_KEY` (optional)
8. Your API will be available at `https://your-app.railway.app`

### 2. Render (Free Tier)

1. Visit [render.com](https://render.com)
2. Connect your GitHub account
3. Click "New" → "Web Service"
4. Select your repository
5. Set:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `OPENAI_API_KEY` (optional)

### 3. Heroku

1. Install Heroku CLI
2. In the backend folder:
```bash
heroku create your-script-writer-api
heroku config:set OPENAI_API_KEY=your_key_here
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 4. DigitalOcean App Platform

1. Visit [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Go to Apps → Create App
3. Connect GitHub and select your repo
4. Choose `backend` as source directory
5. Set environment variables in the app settings

### 5. Vercel (Serverless)

1. Install Vercel CLI: `npm i -g vercel`
2. In the backend folder:
```bash
vercel
```
3. Follow the prompts to deploy

## Environment Variables

For any deployment, you can optionally set:
- `OPENAI_API_KEY`: Your OpenAI API key for AI-powered generation
- `PORT`: Server port (auto-set by most platforms)

## Testing Your Deployment

Once deployed, test your API:

1. Visit `https://your-api-url.com/health` - should return status
2. Use the frontend with your new API URL
3. Run the test script: `python test_api.py`

## Updating Your Frontend

After deploying, update your frontend's API URL:

1. In `index.html`, change the default API URL:
```javascript
const DEFAULT_API_URL = 'https://your-deployed-api-url.com';
```

2. Or users can manually enter the URL in the frontend form

## Cost Considerations

- **Free Options**: Railway, Render, Heroku (limited hours)
- **OpenAI API**: ~$0.002 per script generation
- **Without OpenAI**: Completely free (uses templates)

## Security Notes

For production:
1. Update CORS origins in `main.py` to your frontend domain
2. Add rate limiting
3. Use HTTPS only
4. Consider API key authentication
