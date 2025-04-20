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
# 2. Load Prompt from TXT
# ----------------------------
def load_prompt(file_path="prompt.txt"):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Load the prompt from the external file
base_prompt = load_prompt()

# ----------------------------
# 3. YouTube Script Generation Function
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
    
    # Append the topic to the base prompt
    full_prompt = base_prompt + "\n\nThe topic of the script is: {}.".format(topic)
    
    if reference:
        full_prompt += "\n\nReference Script Excerpts:\n" + reference + "\n\n"
    
    try:
        response = model.generate_content(full_prompt)
        if response.text:
            return response.text.strip()
        else:
            return "No content generated. Please try again."
    except Exception as e:
        return f"Error generating script: {e}"

# ----------------------------
# 4. Configure Gemini 2.0 Flash API

api_key = st.secrets["google_api"]

# Configure the API
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")
# ----------------------------
# 5. Streamlit App Layout & Settings
# ----------------------------
st.set_page_config(page_title="YouTube Script Generator", page_icon="🎬")
st.title("🎬 YouTube Script Generator")
st.caption("Powered by Gemini 2.0 Flash with Retrieval-Augmented Generation")

# Sidebar: Additional Settings
st.sidebar.header("Settings")
script_length = st.sidebar.selectbox("Script Length", ["Short", "Medium", "Long"])
# (You could further modify the prompt based on the chosen length)

# ----------------------------
# 6. Session State & Script Storage
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
# 7. Topic Input and Script Generation
# ----------------------------
topic_input = st.text_input("Enter the topic for your YouTube script:")

if st.button("Generate Script") and topic_input:
    with st.spinner("Generating script..."):
        generated_script = generate_youtube_script(topic_input)
    st.session_state.current_script = generated_script
    st.session_state.script_history.append(generated_script)
    st.success("Script generated successfully!")

# ----------------------------
# 8. Display the Generated Script and Download Option
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
# 9. Modify a Specific Paragraph
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
# 10. Display Full Script History (if needed)
# ----------------------------
if st.session_state.script_history:
    st.subheader("Previously Generated Scripts:")
    for idx, script in enumerate(st.session_state.script_history, start=1):
        st.text_area(f"Script {idx}", script, height=150)

# ----------------------------
# 11. Close App Button
# ----------------------------
if st.sidebar.button("Close App"):
    st.warning("The app is closing...")
    os._exit(0)
