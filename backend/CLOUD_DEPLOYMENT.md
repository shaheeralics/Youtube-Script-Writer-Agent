# 🚀 Cloud Deployment Guide for YouTube Script Writer API

## Ready-to-Deploy Cloud Platforms

### 1. 🌟 Railway (Recommended - Easiest)

**Why Railway?**
- Free tier with 500 hours/month
- Automatic deployments from GitHub
- Built-in environment variables
- Custom domains
- Zero configuration

**Steps:**
1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `Youtube-Script-Writer-Agent` repository
5. Set **Root Directory**: `backend`
6. Add environment variables:
   - `GOOGLE_API_KEY`: Your Gemini API key
   - `OPENAI_API_KEY`: Your OpenAI key (optional)
7. Deploy! Your API will be at `https://your-app.railway.app`

### 2. 🔥 Render (Free Tier)

**Steps:**
1. Visit [render.com](https://render.com)
2. Connect GitHub account
3. "New" → "Web Service"
4. Select your repository
5. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: 3.9+
6. Add environment variables in dashboard

### 3. 🚀 Vercel (Serverless)

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. In backend folder: `vercel`
3. Add `vercel.json`:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### 4. ⚡ Heroku

```bash
# In backend folder
heroku create your-script-writer-api
heroku config:set GOOGLE_API_KEY=your_key_here
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 5. 🌊 DigitalOcean App Platform

1. Create account at [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Apps → Create App → GitHub
3. Select repo, set `backend` as source
4. App-level environment variables in settings

## 🔑 Getting API Keys

### Google Gemini API (Recommended)
1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Get API Key → Create API key
3. Copy the key for `GOOGLE_API_KEY`

### OpenAI API (Optional)
1. Visit [platform.openai.com](https://platform.openai.com)
2. API Keys → Create new secret key
3. Copy for `OPENAI_API_KEY`

## 🧪 Testing Your Deployment

After deployment, test these endpoints:

### Health Check
```
GET https://your-api-url.com/health
```

### Generate Script
```bash
curl -X POST "https://your-api-url.com/generate-script" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence in Pakistan",
    "style": "techfela_short",
    "language": "roman_urdu"
  }'
```

## 📱 Update Frontend

After deploying, update your frontend:

1. Edit `index.html`
2. Change the default API URL:
```javascript
const DEFAULT_API_URL = 'https://your-deployed-api-url.com';
```

## 💰 Cost Breakdown

### Free Tier Options:
- **Railway**: 500 hours/month free
- **Render**: 750 hours/month free
- **Vercel**: Generous free tier
- **Heroku**: 550 hours/month free

### API Costs:
- **Google Gemini**: Very generous free tier
- **OpenAI**: ~$0.002 per script
- **No API Keys**: 100% free (uses templates)

## 🔒 Production Security

For production deployment:

1. **Update CORS** in `main.py`:
```python
allow_origins=["https://yourdomain.com"]  # Your frontend domain
```

2. **Add Rate Limiting**:
```python
# Add to requirements.txt
slowapi==0.1.9

# Add to main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/generate-script")
@limiter.limit("10/minute")  # 10 requests per minute
async def generate_script(request: Request, script_request: ScriptRequest):
    # existing code
```

3. **Environment Variables Only**:
   - Never commit API keys to code
   - Use platform environment variable settings

## 🚀 Quick Start Commands

```bash
# Test locally first
cd backend
pip install -r requirements.txt
python main.py

# Deploy to Railway (fastest)
# 1. Push to GitHub
# 2. Connect Railway to GitHub
# 3. Deploy!

# Deploy to Render
# 1. Connect GitHub
# 2. Set build/start commands
# 3. Add environment variables

# Deploy to Vercel
npm i -g vercel
cd backend
vercel
```

## 🔄 Auto-Updates

All platforms support automatic deployment from GitHub:
1. Push changes to your repository
2. Platform automatically redeploys
3. Zero downtime deployments

## 📞 Support

If you need help:
1. Check platform documentation
2. Test with `/health` endpoint
3. Check environment variables
4. Review deployment logs

Your YouTube Script Writer API will be live and ready to generate amazing scripts! 🎬✨
