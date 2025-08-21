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
    title="TechFela YouTube Script Writer API",
    description="AI-powered YouTube script generation for TechFela channel",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Request/Response models
class ScriptRequest(BaseModel):
    topic: str
    video_type: str = "short"  # short (60-90 secs), long (3-6 mins)

class ScriptResponse(BaseModel):
    script: str
    word_count: int
    estimated_duration: str

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_techfela_script(topic: str, video_type: str = "short") -> str:
    """Generate script using TechFela prompts and Gemini AI"""
    
    try:
        # Choose appropriate prompt based on video type
        if video_type == "short":
            prompt = short_video_prompt  # 60-90 seconds
        else:  # long
            prompt = long_video_prompt   # 3-6 minutes
        
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
        return generate_techfela_template(topic, video_type)
        
    except Exception as e:
        logger.error(f"Error in TechFela script generation: {e}")
        return generate_techfela_template(topic, video_type)

def generate_techfela_template(topic: str, video_type: str) -> str:
    """Generate a TechFela-style template when AI is not available"""
    
    if video_type == "short":
        return f"""Video Title: {topic}: Yeh Kyun Itna Popular Hai? 🤔

(0-15 seconds)
{topic} ke baare mein suna hai? Agar nahi toh aaj tumhein pata chal jayega kyun sab is ke peeche pagal hain!

(15-30 seconds)
Dekho bhai, {topic} actually yeh hai ke... *explains basic concept in simple Urdu*. Lekin masla yeh hai ke log ise samajh nahi pa rahe.

(30-45 seconds)
Pehle zamane mein hum log purane methods use karte the, lekin ab {topic} se sab kuch itna easy ho gaya hai!

(45-60 seconds)
Lekin yahan twist yeh hai - {topic} ke saath ek problem bhi hai. Woh yeh ke sab log ise galat samajh rahe hain.

(60-75 seconds)
Toh conclusion yeh hai ke {topic} zaroori hai, lekin samajhdari se use karna parega.

(75-90 seconds)
Agar video pasand aya toh like kar do, TechFela ko subscribe karna mat bhoolna! Comment mein batao ke tum {topic} use karte ho ya nahi!"""
    
    else:  # Long format (3-6 minutes)
        return f"""Video Title: {topic}: Complete Guide - Sab Kuch Jo Tumhein Jaanna Chahiye! 🔥

(0-30 seconds)
Assalam o Alaikum TechFela family! Aaj hum detail mein baat karenge {topic} ke baare mein. Agar tum tech ke fan ho toh yeh video tumhare liye perfect hai!

(30-90 seconds)
Pehle main batata hun ke {topic} hai kya. Basically yeh ek technology/concept hai jo aaj kal har jagah use ho raha hai. Pakistan mein bhi iska trend barh raha hai.

(90-150 seconds)
{topic} ke main benefits yeh hain:
- Pehla faida: Time save hota hai
- Doosra faida: Efficiency barh jati hai  
- Teesra faida: Cost effective hai

(150-210 seconds)
Lekin har cheez ke kuch disadvantages bhi hote hain. {topic} ke saath main issues yeh hain:
- Privacy concerns
- Technical knowledge chahiye
- Initial setup thoda complex ho sakta hai

(210-270 seconds)
Pakistan mein {topic} ka future kya hai? Main tumhein batata hun ke experts kya keh rahe hain. Agले 2-3 saal mein yeh technology aur bhi common ho jayegi.

(270-330 seconds)
Agar tum {topic} use karna chahte ho toh yeh steps follow karo:
1. Pehle research karo
2. Budget decide karo
3. Slowly slowly implement karo

(330-360 seconds)
Toh dosto, yeh tha complete overview of {topic}. Agar video helpful laga toh like karo, subscribe karo aur bell icon press karna mat bhoolna! Comments mein batao ke tumhara experience kya hai!"""

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "TechFela Script Writer API is running!", "status": "healthy"}

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
    """Generate a YouTube script based on the provided topic and video type"""
    
    try:
        logger.info(f"Generating {request.video_type} script for topic: {request.topic}")
        
        # Validate input
        if not request.topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        if len(request.topic) > 200:
            raise HTTPException(status_code=400, detail="Topic too long (max 200 characters)")
        
        # Generate TechFela script
        script = generate_techfela_script(request.topic, request.video_type)
        
        # Calculate metrics
        word_count = len(script.split())
        
        # Estimate duration based on video type
        if request.video_type == "short":
            estimated_duration = "60-90 seconds"
        else:
            estimated_duration = "3-6 minutes"
        
        logger.info(f"Script generated successfully. Word count: {word_count}")
        
        return ScriptResponse(
            script=script,
            word_count=word_count,
            estimated_duration=estimated_duration
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating script")

async def generate_ai_script(request: ScriptRequest) -> str:
    """Generate script using OpenAI API - simplified for TechFela only"""
    
    try:
        # Choose prompt based on video type
        if request.video_type == "short":
            prompt = short_video_prompt
        else:
            prompt = long_video_prompt
            
        full_prompt = f"{prompt}\n\nThe topic of the script is: {request.topic}."
        
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
        logger.error(f"OpenAI API error: {str(e)}")
        # Fallback to template generation
        return generate_techfela_template(request.topic, request.video_type)

def estimate_duration(word_count: int) -> str:
    """Estimate video duration based on word count"""
    minutes = word_count / 150
    
    if minutes < 1.5:
        return "60-90 seconds"
    elif minutes < 6:
        return "3-6 minutes"
    else:
        return "6+ minutes"

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
