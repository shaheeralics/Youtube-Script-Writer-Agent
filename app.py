import os
import streamlit as st
from docx import Document
import google.generativeai as genai
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
    """Convert markdown text to PDF for download using ReportLab (Unicode compatible)"""
    buffer = io.BytesIO()
    
    # Create the PDF object using ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Set default font
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    c.setFont("DejaVuSans", 12)
    
    # Simple markdown parsing
    y_position = height - 40  # Start from top with margin
    
    # Split by paragraphs
    paragraphs = markdown_text.split('\n\n')
    
    for p in paragraphs:
        if p.strip():
            # Check if it's a heading (starts with #)
            if p.strip().startswith('#'):
                heading_level = len(re.match(r'^#+', p.strip()).group())
                heading_text = p.strip()[heading_level:].strip()
                
                if heading_level == 1:
                    c.setFont("DejaVuSans", 16)
                elif heading_level == 2:
                    c.setFont("DejaVuSans", 14)
                else:
                    c.setFont("DejaVuSans", 12)
                
                c.drawString(40, y_position, heading_text)
                y_position -= 20
                c.setFont("DejaVuSans", 12)
            else:
                # Regular paragraph - wrap text to fit page width
                text_obj = c.beginText(40, y_position)
                text_obj.setFont("DejaVuSans", 12)
                
                # Simple text wrapping
                words = p.split()
                line = ""
                for word in words:
                    test_line = line + " " + word if line else word
                    if c.stringWidth(test_line, "DejaVuSans", 12) < width - 80:
                        line = test_line
                    else:
                        text_obj.textLine(line)
                        line = word
                
                if line:
                    text_obj.textLine(line)
                
                c.drawText(text_obj)
                y_position -= 40  # Move down for next paragraph
            
            # Check if we need a new page
            if y_position < 40:
                c.showPage()
                c.setFont("DejaVuSans", 12)
                y_position = height - 40
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()

# Fallback PDF generation function that doesn't use Unicode
def simple_pdf_generation(text):
    """Simple PDF generation without Unicode characters"""
    # Filter out or replace Unicode characters
    filtered_text = text.encode('ascii', 'replace').decode('ascii')
    
    buffer = io.BytesIO()
    
    # Create the PDF object using ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Set default font
    c.setFont("Helvetica", 12)
    
    # Simple text layout
    y_position = height - 40
    
    # Split by paragraphs
    paragraphs = filtered_text.split('\n\n')
    
    for p in paragraphs:
        if p.strip():
            text_obj = c.beginText(40, y_position)
            text_obj.setFont("Helvetica", 12)
            
            # Simple text wrapping
            words = p.split()
            line = ""
            for word in words:
                test_line = line + " " + word if line else word
                if c.stringWidth(test_line, "Helvetica", 12) < width - 80:
                    line = test_line
                else:
                    text_obj.textLine(line)
                    line = word
            
            if line:
                text_obj.textLine(line)
            
            c.drawText(text_obj)
            y_position -= 40
            
            if y_position < 40:
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 40
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()

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
    
    # Show only preview (no raw text)
    st.subheader("Preview:")
    html = convert_markdown_to_html(st.session_state.current_script)
    st.markdown(html, unsafe_allow_html=True)
    
    # Edit button/expander (hidden by default)
    with st.expander("Edit Script", expanded=False):
        updated_script = st.text_area("Your YouTube Script (editable):", st.session_state.current_script, height=300)
        # Save any manual edits back to the session state
        if updated_script != st.session_state.current_script:
            st.session_state.current_script = updated_script
            st.experimental_rerun()  # Refresh to show updated preview
    
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
        # Download as PDF with error handling
        try:
            # First try with full Unicode support
            try:
                pdf_data = markdown_to_pdf(st.session_state.current_script)
            except Exception as e:
                # Fallback to simple PDF generation on error
                st.warning("Using simplified PDF export due to special characters in text")
                pdf_data = simple_pdf_generation(st.session_state.current_script)
                
            st.download_button(
                label="Download as PDF",
                data=pdf_data,
                file_name="youtube_script.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Could not generate PDF: {str(e)}")

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
