import os
import streamlit as st
from docx import Document
import google.generativeai as genai
import io
from fpdf import FPDF
import markdown
import re
from bs4 import BeautifulSoup

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
# 5. Helper Functions for Markdown and PDF Conversion
# ----------------------------
def convert_markdown_to_html(markdown_text):
    """Convert markdown text to HTML for preview display"""
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)
    return html

def markdown_to_pdf(markdown_text):
    """Convert markdown text to PDF for download"""
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=12)
    
    # Simple markdown parsing for basic formatting
    # Split by paragraphs
    paragraphs = markdown_text.split('\n\n')
    
    for p in paragraphs:
        if p.strip():
            # Check if it's a heading (starts with #)
            if p.strip().startswith('#'):
                heading_level = len(p.split(' ')[0])  # Count the number of #
                heading_text = p.replace('#', '', heading_level).strip()
                if heading_level == 1:
                    pdf.set_font("Arial", 'B', 16)
                elif heading_level == 2:
                    pdf.set_font("Arial", 'B', 14)
                else:
                    pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, txt=heading_text, ln=True)
                pdf.set_font("Arial", size=12)  # Reset font
            else:
                # Regular paragraph
                # Handle bold and italic basic formatting
                processed_text = p
                
                # Handle bold text (enclosed in ** or __)
                bold_pattern = r'\*\*(.*?)\*\*|__(.*?)__'
                for match in re.finditer(bold_pattern, p):
                    bold_text = match.group(1) or match.group(2)
                    processed_text = processed_text.replace(match.group(0), bold_text)
                
                # Add text to PDF with line breaks for long paragraphs
                pdf.multi_cell(0, 10, txt=processed_text)
                pdf.ln(5)  # Add some space between paragraphs
    
    # Convert PDF to bytes
    pdf_bytes = io.BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    
    return pdf_bytes.getvalue()

# ----------------------------
# 6. Streamlit App Layout & Settings
# ----------------------------
st.set_page_config(page_title="YouTube Script Generator", page_icon="🎬")
st.title("🎬 YouTube Script Generator")
st.caption("Powered by Gemini 2.0 Flash with Retrieval-Augmented Generation")

# Sidebar: Additional Settings
st.sidebar.header("Settings")
script_length = st.sidebar.selectbox("Script Length", ["Short", "Medium", "Long"])
# (You could further modify the prompt based on the chosen length)

# ----------------------------
# 7. Session State & Script Storage
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
# 8. Topic Input and Script Generation
# ----------------------------
topic_input = st.text_input("Enter the topic for your YouTube script:")

if st.button("Generate Script") and topic_input:
    with st.spinner("Generating script..."):
        generated_script = generate_youtube_script(topic_input)
    st.session_state.current_script = generated_script
    st.session_state.script_history.append(generated_script)
    st.success("Script generated successfully!")

# ----------------------------
# 9. Display the Generated Script and Download Option
# ----------------------------
if st.session_state.current_script:
    st.subheader("Generated Script:")
    # Text area for editing the script
    updated_script = st.text_area("Your YouTube Script (editable):", st.session_state.current_script, height=300)
    # Save any manual edits back to the session state
    st.session_state.current_script = updated_script
    
    # Preview section - Display the script with markdown formatting
    st.subheader("Preview:")
    html = convert_markdown_to_html(st.session_state.current_script)
    st.markdown(html, unsafe_allow_html=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        # Download as text file
        st.download_button(
            label="Download as Text",
            data=st.session_state.current_script,
            file_name="youtube_script.txt",
            mime="text/plain"
        )
    with col2:
        # Download as PDF
        pdf_data = markdown_to_pdf(st.session_state.current_script)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="youtube_script.pdf",
            mime="application/pdf"
        )

# ----------------------------
# 10. Modify a Specific Paragraph
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
# 11. Display Full Script History (if needed)
# ----------------------------
if st.session_state.script_history:
    st.subheader("Previously Generated Scripts:")
    for idx, script in enumerate(st.session_state.script_history, start=1):
        st.text_area(f"Script {idx}", script, height=150)

# ----------------------------
# 12. Close App Button
# ----------------------------
if st.sidebar.button("Close App"):
    st.warning("The app is closing...")
    os._exit(0)
