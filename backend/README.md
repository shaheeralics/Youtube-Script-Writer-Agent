# YouTube Script Writer Backend

A FastAPI-powered backend service for generating AI-driven YouTube scripts.

## Features

- **AI-Powered Generation**: Uses OpenAI GPT models for intelligent script creation
- **Fallback Templates**: Works even without API keys using template-based generation
- **Flexible Parameters**: Customize style, duration, and target audience
- **CORS Enabled**: Ready for frontend integration
- **Health Monitoring**: Built-in health check endpoints
- **Professional Structure**: Well-organized scripts with timing and visual cues

## API Endpoints

### `POST /generate-script`
Generate a YouTube script based on provided parameters.

**Request Body:**
```json
{
  "topic": "Machine Learning for Beginners",
  "style": "educational",
  "duration": "medium", 
  "target_audience": "beginners"
}
```

**Response:**
```json
{
  "script": "Full script content...",
  "word_count": 1250,
  "estimated_duration": "5-10 minutes",
  "sections": ["Introduction", "Main Content", "Conclusion"]
}
```

### `GET /health`
Health check endpoint with system status.

## Parameters

### Style Options:
- `educational` - Teaching and explaining concepts
- `entertainment` - Fun and engaging content
- `tutorial` - Step-by-step instructions
- `review` - Analysis and opinions

### Duration Options:
- `short` - 2-5 minutes (300-750 words)
- `medium` - 5-10 minutes (750-1500 words)
- `long` - 10+ minutes (1500+ words)

### Target Audience:
- `general` - Accessible to everyone
- `beginners` - Simple explanations
- `advanced` - Technical depth
- `kids` - Child-friendly language

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
# Create .env file
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Deployment

This backend can be deployed to:
- **Railway**: Connect GitHub repo and deploy automatically
- **Heroku**: Push to Heroku with Procfile
- **DigitalOcean App Platform**: Deploy from GitHub
- **AWS Lambda**: With Mangum adapter
- **Google Cloud Run**: Containerized deployment

## Environment Variables

- `OPENAI_API_KEY` (optional): For AI-powered generation
- `PORT` (optional): Server port (defaults to 8000)

## CORS Configuration

The API allows cross-origin requests from any domain. For production, update the `allow_origins` in `main.py` to specific domains:

```python
allow_origins=["https://yourdomain.com"]
```
