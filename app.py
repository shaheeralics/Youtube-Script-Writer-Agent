import os
import streamlit as st
from docx import Document
import google.generativeai as genai

# ----------------------------
# 1. Load Reference Scripts from DOCX
# ----------------------------
def load_sample_scripts(file_path="sample_scripts.docx"):
    if not os.path.exists(file_path):
        return []
    document = Document(file_path)
    scripts = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return scripts

sample_scripts = load_sample_scripts()  # Reads from sample_scripts.docx

# ----------------------------
# 2. YouTube Script Generation Function
# ----------------------------
def generate_youtube_script(topic):
    """
    Generates a YouTube script using Gemini 2.0 Flash.
    It uses a base prompt with a preset context and (optionally) a reference excerpt.
    """
    # Optionally find a reference excerpt from the sample scripts
    reference = ""
    if sample_scripts:
        reference = max(sample_scripts, key=lambda s: s.lower().count(topic.lower()))
    
    # Define the prompt template for your Youtube Script Writer Agent
    base_prompt = (
        '''
        🎬 Prompt Title:
“Roman Urdu mein Mazedaar, Smart aur Viral Script banao – TechFela Style”

📌 Role & Vibe:
Tum ho ek fun, sharp aur relatable scriptwriter jo short-form videos banata hai (YouTube Shorts, Reels, TikTok) modern desi audience ke liye – especially Pakistan/South Asia.

🗣️ Tone & Language:
Baat-cheet jaisi tone – thori witty, thori sarcastic

Roman Urdu main likho, with light English mix

Jaise Lahore, Karachi, ya Islamabad ka banda casually baat kar raha ho

Memes, exaggeration aur pop culture references zaroori hain

🎯 Structure:
00:00:00 – Hook: Shocking ya funny question/se kahani shuru karo

00:00:15 – Context: Topic ka thoda background do – but jaldi

00:00:30 – Points: 2-3 baatain ya reasons – mazedaar examples ke sath

00:01:10 – End: Ek punchline ya twist maaro + sarcastic moral

Creative shoutout for TechFela at the end – fun way mein

📏 Format:
Max 90 seconds (~150–180 words)

Timestamps zaroor dena har 15–20 sec ke baad

Tone: relatable + funny + informative

Style: Script should feel like ek dost apne doston se baat kar raha ho

🎥 Topics Examples:
“Wireless charging itna slow kyun hai – jaise chai banate waqt crush ka reply”

“Elon Musk aur censorship ka chakker kya hai?”

“Smartphones ki asli battery life vs. unki acting skills”

❌ Important:
No “Here’s the script” type lines

Sirf clean, direct, and catchy script chahiye

Script mein TechFela ka mention ho – but naturally and non-cringe

Use these guidelines to generate a viral, relatable, and funny script that feels authentic and original."
"Now generate a script on the topic: "
        '''
        "The topic is: {}.\n\n"
    ).format(topic)
    
    if reference:
        base_prompt += "Reference Script Excerpts:\n" + reference + "\n\n"
    
    try:
        response = model.generate_content(base_prompt)
        if response.text:
            return response.text.strip()
        else:
            return "No content generated. Please try again."
    except Exception as e:
        return f"Error generating script: {e}"

# ----------------------------
# 3. Configure Gemini 2.0 Flash API

api_key = st.secrets["google_api"]

# Configure the API
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")
# ----------------------------
# 4. Streamlit App Layout & Settings
# ----------------------------
st.set_page_config(page_title="YouTube Script Generator", page_icon="🎬")
st.title("🎬 YouTube Script Generator")
st.caption("Powered by Gemini 2.0 Flash with Retrieval-Augmented Generation")

# Sidebar: Additional Settings
st.sidebar.header("Settings")
script_length = st.sidebar.selectbox("Script Length", ["Short", "Medium", "Long"])
# (You could further modify the prompt based on the chosen length)

# ----------------------------
# 5. Session State & Script Storage
# ----------------------------
if "current_script" not in st.session_state:
    st.session_state.current_script = ""
if "script_history" not in st.session_state:
    st.session_state.script_history = []

if st.button("🆕 New Script"):
    st.session_state.current_script = ""
    st.session_state.script_history = []
    st.experimental_rerun()

# ----------------------------
# 6. Topic Input and Script Generation
# ----------------------------
topic_input = st.text_input("Enter the topic for your YouTube script:")

if st.button("Generate Script") and topic_input:
    with st.spinner("Generating script..."):
        generated_script = generate_youtube_script(topic_input)
    st.session_state.current_script = generated_script
    st.session_state.script_history.append(generated_script)
    st.success("Script generated successfully!")

# ----------------------------
# 7. Display the Generated Script and Download Option
# ----------------------------
if st.session_state.current_script:
    st.subheader("Generated Script:")
    updated_script = st.text_area("Your YouTube Script (editable):", st.session_state.current_script, height=300)
    # Save any manual edits back to the session state
    st.session_state.current_script = updated_script

    # Download button: Download the current script as a text file
    st.download_button(
        label="Download Script",
        data=st.session_state.current_script,
        file_name="youtube_script.txt",
        mime="text/plain"
    )

# ----------------------------
# 8. Modify a Specific Paragraph
# ----------------------------
if st.session_state.current_script:
    st.subheader("Modify a Specific Paragraph")
    # Split the script into paragraphs using double newline as a separator
    paragraphs = [p for p in st.session_state.current_script.split("\n\n") if p.strip()]
    if paragraphs:
        # Allow the user to select which paragraph to edit
        para_idx = st.selectbox("Select Paragraph to Modify", range(1, len(paragraphs) + 1), format_func=lambda x: f"Paragraph {x}")
        new_text = st.text_area("Edit Selected Paragraph", paragraphs[para_idx - 1], height=100)
        
        if st.button("Update Paragraph"):
            # Update the selected paragraph and reassemble the script
            paragraphs[para_idx - 1] = new_text.strip()
            updated_full_script = "\n\n".join(paragraphs)
            st.session_state.current_script = updated_full_script
            st.success("Paragraph updated!")
            st.experimental_rerun()

# ----------------------------
# 9. Display Full Script History (if needed)
# ----------------------------
if st.session_state.script_history:
    st.subheader("Previously Generated Scripts:")
    for idx, script in enumerate(st.session_state.script_history, start=1):
        st.text_area(f"Script {idx}", script, height=150)

# ----------------------------
# 10. Close App Button
# ----------------------------
if st.sidebar.button("Close App"):
    st.warning("The app is closing...")
    os._exit(0)
