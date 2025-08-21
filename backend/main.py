from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import time
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YouTube Script Writer API",
    description="AI-powered YouTube script generation service",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Request/Response models
class ScriptRequest(BaseModel):
    topic: str
    style: str = "educational"  # educational, entertainment, tutorial, review
    duration: str = "medium"    # short (2-5 min), medium (5-10 min), long (10+ min)
    target_audience: str = "general"  # general, beginners, advanced, kids

class ScriptResponse(BaseModel):
    script: str
    word_count: int
    estimated_duration: str
    sections: list

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_script_prompt(topic: str, style: str, duration: str, target_audience: str) -> str:
    """Generate a detailed prompt for script creation based on parameters"""
    
    duration_guidelines = {
        "short": "2-5 minutes (300-750 words)",
        "medium": "5-10 minutes (750-1500 words)", 
        "long": "10+ minutes (1500+ words)"
    }
    
    style_guidelines = {
        "educational": "Focus on teaching and explaining concepts clearly with examples",
        "entertainment": "Make it engaging, fun, and entertaining with humor and storytelling",
        "tutorial": "Provide step-by-step instructions with practical demonstrations",
        "review": "Give honest opinions, pros/cons, and detailed analysis"
    }
    
    audience_guidelines = {
        "general": "Use accessible language that anyone can understand",
        "beginners": "Explain basic concepts thoroughly with simple examples", 
        "advanced": "Use technical terminology and dive deep into complex topics",
        "kids": "Use simple words, fun examples, and engaging storytelling"
    }
    
    return f"""Create a professional YouTube script about "{topic}".

REQUIREMENTS:
- Target Duration: {duration_guidelines.get(duration, duration_guidelines['medium'])}
- Style: {style_guidelines.get(style, style_guidelines['educational'])}
- Target Audience: {audience_guidelines.get(target_audience, audience_guidelines['general'])}

STRUCTURE:
1. **Hook** (First 15 seconds) - Grab attention immediately
2. **Introduction** - Introduce yourself and the topic
3. **Main Content** - Core information broken into clear sections
4. **Examples/Demonstrations** - Practical applications
5. **Conclusion** - Summarize key points
6. **Call to Action** - Subscribe, like, comment prompts

TONE:
- Conversational and engaging
- Appropriate for YouTube platform
- Match the specified style and audience

FORMAT:
- Use clear section headers
- Include timing suggestions
- Add [VISUAL CUE] notes where relevant
- Include engagement prompts throughout

Make it compelling, well-structured, and optimized for YouTube success!"""

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "YouTube Script Writer API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.post("/generate-script", response_model=ScriptResponse)
async def generate_script(request: ScriptRequest):
    """Generate a YouTube script based on the provided topic and parameters"""
    
    try:
        logger.info(f"Generating script for topic: {request.topic}")
        
        # Validate input
        if not request.topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        if len(request.topic) > 200:
            raise HTTPException(status_code=400, detail="Topic too long (max 200 characters)")
        
        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            # Fallback to template-based generation
            logger.warning("OpenAI API key not configured, using template generation")
            script = generate_template_script(request)
        else:
            # Use OpenAI for script generation
            script = await generate_ai_script(request)
        
        # Calculate metrics
        word_count = len(script.split())
        estimated_duration = estimate_duration(word_count)
        sections = extract_sections(script)
        
        logger.info(f"Script generated successfully. Word count: {word_count}")
        
        return ScriptResponse(
            script=script,
            word_count=word_count,
            estimated_duration=estimated_duration,
            sections=sections
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating script")

async def generate_ai_script(request: ScriptRequest) -> str:
    """Generate script using OpenAI API"""
    
    try:
        prompt = get_script_prompt(request.topic, request.style, request.duration, request.target_audience)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert YouTube script writer who creates engaging, well-structured content that drives views and engagement."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        # Fallback to template generation
        return generate_template_script(request)

def generate_template_script(request: ScriptRequest) -> str:
    """Generate script using templates when AI is not available"""
    
    topic = request.topic
    style = request.style
    
    script = f"""# {topic}

## Hook (0:00-0:15)
Hey everyone! Have you ever wondered about {topic}? Well, you're in for a treat because today we're diving deep into everything you need to know about this fascinating subject. Stick around because I guarantee you'll learn something new!

## Introduction (0:15-0:45)
Welcome back to the channel! I'm your host, and today we're exploring {topic}. Whether you're a complete beginner or looking to expand your knowledge, this video has something valuable for everyone.

[VISUAL CUE: Show engaging graphics or title screen]

## Main Content

### What is {topic}? (0:45-2:00)
Let me start by explaining what {topic} actually is. {topic} is [detailed explanation]. This concept has been gaining attention because [relevant reasons].

### Why Should You Care? (2:00-3:30)
Here are the key reasons why {topic} matters:

• **Reason 1**: [Practical benefit or application]
• **Reason 2**: [Future potential or relevance]  
• **Reason 3**: [Personal or professional impact]

[VISUAL CUE: Show supporting charts, images, or examples]

### Getting Started (3:30-5:00)
If you're interested in exploring {topic}, here's how to begin:

1. **Step 1**: [First actionable step with explanation]
2. **Step 2**: [Second step with practical advice]
3. **Step 3**: [Third step to build momentum]

### Common Mistakes to Avoid (5:00-6:00)
Before we go further, let me share some common pitfalls people encounter:

• **Mistake 1**: [Common error and how to avoid it]
• **Mistake 2**: [Another frequent issue]
• **Mistake 3**: [Third mistake with solution]

### Pro Tips (6:00-7:00)
Here are some advanced strategies that most people don't know:
- [Expert tip 1]
- [Expert tip 2]
- [Expert tip 3]

[VISUAL CUE: Highlight these tips with special graphics]

## Real-World Examples (7:00-8:00)
Let me show you some concrete examples of {topic} in action:
[Specific examples relevant to the topic with explanations]

## Conclusion (8:00-8:30)
To wrap up, {topic} is incredibly powerful when you understand how to apply it correctly. The key takeaways from today's video are:

1. [Key insight 1]
2. [Key insight 2]
3. [Key insight 3]

## Call to Action (8:30-9:00)
If you found this video helpful, please give it a thumbs up - it really helps the channel grow! 

What's your experience with {topic}? Drop your thoughts in the comments below, and I'll make sure to respond to as many as possible.

Don't forget to subscribe and hit that notification bell for more content like this. I've got some exciting videos coming up that you won't want to miss!

Until next time, keep learning and stay curious!

[VISUAL CUE: End screen with subscribe button and related videos]

---
*Generated by YouTube Script Writer AI*
*Word count: Approximately {len(topic.split()) * 50} words*"""

    return script

def estimate_duration(word_count: int) -> str:
    """Estimate video duration based on word count (assuming 150 words per minute)"""
    minutes = word_count / 150
    
    if minutes < 2:
        return "1-2 minutes"
    elif minutes < 5:
        return "3-5 minutes"
    elif minutes < 10:
        return "5-10 minutes"
    elif minutes < 15:
        return "10-15 minutes"
    else:
        return "15+ minutes"

def extract_sections(script: str) -> list:
    """Extract section titles from the script"""
    sections = []
    lines = script.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('##'):
            # Remove markdown and timing info
            section = line.replace('##', '').strip()
            if '(' in section and ')' in section:
                section = section.split('(')[0].strip()
            sections.append(section)
    
    return sections

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
