# 🎬 TechFela YouTube Script Writer - Railway Ready

Simple FastAPI backend for generating TechFela YouTube scripts in Roman Urdu.

## 🚀 Quick Deploy to Railway

1. **Fork/Clone this repo**
2. **Go to [railway.app](https://railway.app)**
3. **Connect GitHub & Deploy**:
   - New Project → Deploy from GitHub
   - Select this repository
   - Set **Root Directory**: `backend`
4. **Add API Key** (optional):
   - Variables tab → Add `GOOGLE_API_KEY`
   - Get free key from [aistudio.google.com](https://aistudio.google.com)
5. **Done!** Your API will be live at `https://your-app.railway.app`

## 📱 Features

- **Short Videos**: 60-90 second TechFela scripts in Roman Urdu
- **Long Videos**: 3-6 minute detailed TechFela content
- **AI Powered**: Uses Google Gemini (with OpenAI fallback)
- **Template Fallback**: Works even without API keys
- **Sample Scripts**: Includes your existing TechFela prompts and samples

## 🧪 Test Your Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# Generate script
curl -X POST "https://your-app.railway.app/generate-script" \
  -H "Content-Type: application/json" \
  -d '{"topic": "ChatGPT in Pakistan", "video_type": "short"}'
```

## 📁 Files Included

- `main.py` - FastAPI application
- `requirements.txt` - Dependencies
- `Procfile` - Railway deployment config
- `prompt*.txt` - Your TechFela prompts
- `sample_scripts.docx` - Reference scripts

## 💰 Cost

- **Railway**: Free tier (500 hours/month)
- **Google Gemini**: Free tier (generous limits)
- **Total**: $0 for most users

## 📞 Support

Your backend will automatically:
- Install all dependencies
- Load your prompts and samples
- Start the API server
- Handle TechFela script generation

Ready to deploy! 🚀
