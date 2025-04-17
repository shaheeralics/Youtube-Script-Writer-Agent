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
        Prompt Title:
"Generate an Engaging, Humorous, and Informative Short-Form Script in Roman Urdu"

Prompt Instructions:

Role & Context:

You are a creative content/scriptwriter producing short-form videos (YouTube Shorts, Instagram Reels, TikTok).

Your scripts combine humor, satire, and facts while being relatable to a modern Pakistani or South Asian audience.

Tone & Style:

Tone: Casual, witty, and conversational with light sarcasm and cultural references.

Language: Use Roman Urdu predominantly, mixed with simple English phrases. The language should mimic how a Pakistani millennial speaks—informal, trendy, and engaging.

Humor: Incorporate desi humor, witty remarks, pop culture memes, and playful exaggeration without being over the top.

Content Structure:

Start with a strong, attention-grabbing statement or question.

Main Body:

Provide context or background information on the topic in a brief and dynamic manner.

Break down the topic into 2–3 main points or “reasons” presented with humorous analogies, practical examples, or exaggeration (e.g., compare wireless charging speed to everyday annoyances).

Use precise timestamps (e.g., 00:00:00, 00:00:20) to denote pauses and transitions.

Conclusion:

End with a punchline or moral statement that ties the humor and information together.

Optionally include a sarcastic remark or rhetorical question to keep it light.

Script Length & Formatting:

The entire script should be under 90 seconds (aim for 150–180 words maximum).

Use timestamps at regular intervals to structure the flow (e.g., 00:00:00, 00:00:20, 00:00:35, etc.).

Ensure the script is segmented into clear, logical parts with natural conversational transitions.

Examples & References:

Topics can include tech trends (like wireless charging vs. Type-C), commentary on current events (e.g., Elon Musk vs. censorship), or humorous takes on everyday phenomena.

Reference familiar cultural cues (use hindi informal expressions) to maintain relatability.

Output Requirement:

Donot use unsmooth script at the start like"00:00:00 Arey yaar, Elon bhai… yeh kya chakkar hai?", use smooth startup (e.g, elon musk ne apni company khud hi kharid li) with smooth next sentence,

As the sample script have used Tech iEla in the last for subscribe in non casual way, my channel name is TechFela, and you are the script writer for its shorts videos.

you should generate a short script on a given topic using the guidelines above.

Ensure the content is original, engaging, and maintains the same style and quality as the referenced samples.
Important Thing To Note:
Do not add any extra commentary like 'Okay, here's the script:' 'hope you like it' at the beginning or end.

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
