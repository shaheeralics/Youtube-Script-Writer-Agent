from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import time
import logging
from docx import Document
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Load Reference Scripts and Prompts
# ----------------------------
def load_sample_scripts(file_path="sample_scripts.docx"):
    """Load sample scripts from DOCX file"""
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Sample scripts file not found: {file_path}")
            return []
        document = Document(file_path)
        scripts = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        logger.info(f"Loaded {len(scripts)} sample script paragraphs")
        return scripts
    except Exception as e:
        logger.error(f"Error loading sample scripts: {e}")
        return []

def load_prompt(file_path="prompt.txt"):
    """Load prompt from TXT file"""
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Prompt file not found: {file_path}")
            return ""
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            logger.info(f"Loaded prompt from {file_path}")
            return content
    except Exception as e:
        logger.error(f"Error loading prompt: {e}")
        return ""

# Load prompts and samples on startup
base_prompt = load_prompt("prompt.txt")
short_video_prompt = load_prompt("prompt that already worked no 2.txt")
long_video_prompt = load_prompt("prompt long Video.txt")
sample_scripts = load_sample_scripts("sample_scripts.docx")

# Initialize Gemini AI if API key is available
gemini_model = None
if os.getenv("GOOGLE_API_KEY"):
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        gemini_model = genai.GenerativeModel("gemini-2.0-flash")
        logger.info("Gemini AI initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini AI: {e}")

# Initialize OpenAI if API key is available
openai_client = None
if os.getenv("OPENAI_API_KEY"):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai_client = openai
        logger.info("OpenAI initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI: {e}")

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
    style: str = "educational"  # educational, entertainment, tutorial, review, techfela_short, techfela_long
    duration: str = "medium"    # short (2-5 min), medium (5-10 min), long (10+ min)
    target_audience: str = "general"  # general, beginners, advanced, kids
    language: str = "english"  # english, roman_urdu

class ScriptResponse(BaseModel):
    script: str
    word_count: int
    estimated_duration: str
    sections: list

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_techfela_script(topic: str, style: str = "techfela_short") -> str:
    """Generate script using TechFela prompts and Gemini AI"""
    
    try:
        # Choose appropriate prompt based on style
        if style == "techfela_short":
            prompt = short_video_prompt
        elif style == "techfela_long":
            prompt = long_video_prompt
        else:
            prompt = base_prompt
        
        # Find relevant reference from sample scripts
        reference = ""
        if sample_scripts and topic:
            # Find the most relevant sample script based on topic keywords
            topic_lower = topic.lower()
            reference = max(sample_scripts, key=lambda s: sum(word in s.lower() for word in topic_lower.split()))
        
        # Construct full prompt
        full_prompt = f"{prompt}\n\nThe topic of the script is: {topic}."
        
        if reference and len(reference) > 50:  # Only add if we have substantial reference
            full_prompt += f"\n\nReference Script Excerpt:\n{reference}\n\n"
        
        # Try Gemini first, then fallback to OpenAI
        if gemini_model:
            try:
                logger.info("Generating script with Gemini AI")
                response = gemini_model.generate_content(full_prompt)
                if response.text:
                    return response.text.strip()
            except Exception as e:
                logger.error(f"Gemini generation failed: {e}")
        
        # Fallback to OpenAI
        if openai_client:
            try:
                logger.info("Generating script with OpenAI")
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a creative scriptwriter for TechFela YouTube channel that creates engaging, humorous content in Roman Urdu for a Pakistani audience."},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"OpenAI generation failed: {e}")
        
        # Ultimate fallback to template
        return generate_techfela_template(topic, style)
        
    except Exception as e:
        logger.error(f"Error in TechFela script generation: {e}")
        return generate_techfela_template(topic, style)

def generate_techfela_template(topic: str, style: str) -> str:
    """Generate a TechFela-style template when AI is not available"""
    
    if style == "techfela_short":
        return f"""Video Title: {topic}: Yeh Kyun Itna Popular Hai? 🤔

(0-10 seconds)
{topic} ke baare mein suna hai? Agar nahi toh aaj tumhein pata chal jayega kyun sab is ke peeche pagal hain!

(10-25 seconds)
Dekho bhai, {topic} actually yeh hai ke... *explains basic concept in simple Urdu*. Lekin masla yeh hai ke log ise samajh nahi pa rahe.

(25-40 seconds)
Pehle zamane mein hum log *old method* use karte the, lekin ab {topic} se sab kuch itna easy ho gaya hai ke bachpan ke din yaad aa gaye!

(40-55 seconds)
Lekin yahan twist yeh hai - {topic} ke saath ek problem bhi hai. Woh yeh ke... *mentions common issue*

(55-75 seconds)
Toh conclusion yeh hai ke {topic} zaroori hai, lekin samajhdari se use karna parega. Warna phir wohi purana drama!

(75-85 seconds)
Agar tumhein yeh video pasand aya toh like kar do, aur TechFela ko subscribe karna mat bhoolna! Comment mein batao ke tum {topic} use karte ho ya nahi!"""
    
    else:  # Long format
        return f"""# {topic}: Complete Analysis

## Introduction
Assalam o Alaikum TechFela family! Aaj hum baat karenge {topic} ke baare mein jo ke aaj kal har jagah sun rahe hain.

## Main Content

### {topic} Kya Hai?
{topic} basically ek concept/technology hai jo... *detailed explanation in mix of Urdu and English*

### Kyun Important Hai?
- Pehla reason: Modern life mein zaroori
- Doosra reason: Future mein aur bhi important hoga  
- Teesra reason: Pakistan mein bhi adoption barh raha hai

### Real Life Examples
Pakistan mein {topic} ka use:
- Karachi mein...
- Lahore mein...
- Overall trend...

### Pros and Cons
**Fayde:**
- Quick and efficient
- Cost effective ho sakta hai
- User friendly

**Nuksanat:**
- Kuch technical issues
- Privacy concerns
- Learning curve required

## Conclusion
Toh dosto, {topic} definitely future hai, lekin samajh ke saath use karna hoga.

## Call to Action
Video pasand aya ho toh like, subscribe aur bell icon press karna mat bhoolna! Comments mein apna experience share karo!

---
*Generated by TechFela Script Generator*"""

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
        "ai_services": {
            "gemini_configured": gemini_model is not None,
            "openai_configured": openai_client is not None,
        },
        "data_loaded": {
            "base_prompt": bool(base_prompt),
            "short_video_prompt": bool(short_video_prompt),
            "long_video_prompt": bool(long_video_prompt),
            "sample_scripts_count": len(sample_scripts)
        }
    }

@app.post("/generate-script", response_model=ScriptResponse)
async def generate_script(request: ScriptRequest):
    """Generate a YouTube script based on the provided topic and parameters"""
    
    try:
        logger.info(f"Generating script for topic: {request.topic}, style: {request.style}")
        
        # Validate input
        if not request.topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        if len(request.topic) > 200:
            raise HTTPException(status_code=400, detail="Topic too long (max 200 characters)")
        
        # Choose generation method based on style
        if request.style in ["techfela_short", "techfela_long"] or request.language == "roman_urdu":
            # Use TechFela prompts with Gemini/OpenAI
            script = generate_techfela_script(request.topic, request.style)
        elif gemini_model or openai_client:
            # Use AI for other styles
            script = await generate_ai_script(request)
        else:
            # Fallback to template-based generation
            logger.warning("No AI service configured, using template generation")
            script = generate_template_script(request)
        
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
