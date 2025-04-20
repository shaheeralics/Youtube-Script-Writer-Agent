import os
import streamlit as st
from docx import Document
import google.generativeai as genai
import io
import markdown
import re
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

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
    """Convert markdown text to properly formatted PDF preserving formatting"""
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Create styles - only get the sample stylesheet once
    styles = getSampleStyleSheet()
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Create the story (content)
    story = []
    
    # Process each HTML element
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'pre', 'code']):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            heading_level = int(element.name[1])
            # Use the built-in heading styles that come with getSampleStyleSheet()
            if heading_level == 1:
                style_name = 'Heading1'
            elif heading_level == 2:
                style_name = 'Heading2'
            else:
                style_name = 'Heading3'
                
            story.append(Paragraph(element.text, styles[style_name]))
        
        elif element.name == 'p':
            # Process paragraph, handling bold and italic
            text = str(element)
            
            # Replace HTML bold and italic tags with ReportLab equivalents
            text = text.replace('<strong>', '<b>').replace('</strong>', '</b>')
            text = text.replace('<em>', '<i>').replace('</em>', '</i>')
            
            # Strip the outer <p> tags
            text = re.sub(r'^<p>(.*)</p>$', r'\1', text)
            
            # Handle any remaining HTML entities
            text = BeautifulSoup(text, 'html.parser').text
            
            # Create paragraph with styling
            try:
                para = Paragraph(text, styles['Normal'])
                story.append(para)
            except:
                # Fallback for problematic text
                para = Paragraph(text.encode('ascii', 'replace').decode('ascii'), styles['Normal'])
                story.append(para)
        
        elif element.name == 'pre' or element.name == 'code':
            # Format code blocks with monospaced font
            code_text = element.text
            try:
                pre = Preformatted(code_text, styles['Code'])
                story.append(pre)
                story.append(Spacer(1, 6))
            except:
                # Fallback
                pre = Paragraph(code_text.encode('ascii', 'replace').decode('ascii'), styles['Code'])
                story.append(pre)
                story.append(Spacer(1, 6))
    
    # Add content to PDF
    try:
        doc.build(story)
    except Exception as e:
        # Fallback to simple PDF if complex formatting fails
        return simple_pdf_generation(markdown_text)
    
    buffer.seek(0)
    return buffer.getvalue()


# Fallback PDF generation function with basic formatting
def simple_pdf_generation(text):
    """Simple PDF generation with basic formatting"""
    buffer = io.BytesIO()
    
    # Convert markdown to HTML first to parse the formatting
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract text with basic formatting indicators
    formatted_text = ""
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if element.name.startswith('h'):
            level = int(element.name[1])
            formatted_text += f"{'#' * level} {element.text}\n\n"
        else:
            formatted_text += f"{element.text}\n\n"
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create a story with simplified formatting
    story = []
    
    for paragraph in formatted_text.split('\n\n'):
        if paragraph.strip():
            if paragraph.startswith('#'):
                # It's a heading
                heading_level = paragraph.count('#', 0, paragraph.find(' '))
                heading_text = paragraph[heading_level:].strip()
                style_name = f'Heading{min(heading_level, 3)}'
                story.append(Paragraph(heading_text, styles[style_name]))
            else:
                # Regular paragraph
                try:
                    story.append(Paragraph(paragraph, styles['Normal']))
                except:
                    # Handle encoding issues
                    safe_text = paragraph.encode('ascii', 'replace').decode('ascii')
                    story.append(Paragraph(safe_text, styles['Normal']))
    
    # Build the document
    doc.build(story)
    
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
            # Generate PDF with markdown formatting preserved
            pdf_data = markdown_to_pdf(st.session_state.current_script)
            
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
