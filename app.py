import os
import streamlit as st
from docx import Document
import google.generativeai as genai
import io
import markdown
import base64
from xhtml2pdf import pisa

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
    """Convert markdown text to HTML for preview display with enhanced styling"""
    # Convert markdown to HTML with proper styling
    html = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite'])
    
    # Add enhanced styling to make the preview look more professional
    styled_html = f"""
    <div style="padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; background-color: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <style>
            .markdown-preview {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.8;
                color: #333;
            }}
            .markdown-preview h1 {{
                color: #1e88e5;
                font-size: 26px;
                margin-top: 30px;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #f0f0f0;
            }}
            .markdown-preview h2 {{
                color: #0d47a1; 
                font-size: 22px;
                margin-top: 25px;
                margin-bottom: 12px;
                padding-bottom: 8px;
            }}
            .markdown-preview h3 {{
                color: #2962ff;
                font-size: 18px;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            .markdown-preview p {{
                margin: 15px 0;
                font-size: 16px;
                text-align: justify;
            }}
            .markdown-preview strong {{
                font-weight: 600;
                color: #0277bd;
            }}
            .markdown-preview em {{
                font-style: italic;
                color: #444;
            }}
            .markdown-preview code {{
                background-color: #f8f9fa;
                padding: 3px 6px;
                border-radius: 4px;
                border: 1px solid #eee;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
            }}
            .markdown-preview pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #eee;
                overflow-x: auto;
            }}
            .markdown-preview ul, .markdown-preview ol {{
                margin-top: 10px;
                margin-bottom: 10px;
                padding-left: 25px;
            }}
            .markdown-preview li {{
                margin: 5px 0;
            }}
            .markdown-preview blockquote {{
                border-left: 4px solid #64b5f6;
                padding: 10px 15px;
                margin: 15px 0;
                background-color: #e3f2fd;
                font-style: italic;
            }}
            .markdown-preview hr {{
                border: none;
                height: 1px;
                background-color: #e0e0e0;
                margin: 20px 0;
            }}
            .markdown-preview img {{
                max-width: 100%;
                height: auto;
                border-radius: 6px;
                margin: 15px 0;
            }}
            /* Special styling for timestamps in YouTube scripts */
            .markdown-preview p:first-line {{
                font-weight: 500;
            }}
            /* Any text that looks like a timestamp (00:00:00) gets highlighted */
            .markdown-preview p:contains("00:") {{
                background-color: #f1f8e9;
                padding: 5px;
                border-radius: 4px;
            }}
        </style>
        <div class="markdown-preview">
            {html}
        </div>
    </div>
    """
    return styled_html

def convert_html_to_pdf(source_html):
    """Convert HTML to PDF using xhtml2pdf, a pure Python library"""
    result_file = io.BytesIO()
    
    # Add proper HTML structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: letter;
            margin: 1cm;
        }}
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            font-size: 12px;
        }}
        h1 {{
            color: #2c3e50;
            font-size: 24px;
            margin-top: 20px;
        }}
        h2 {{
            color: #3498db;
            font-size: 20px;
            margin-top: 15px;
        }}
        h3 {{
            font-size: 16px;
            margin-top: 10px;
        }}
        p {{
            margin: 10px 0;
        }}
        strong {{
            font-weight: bold;
        }}
        em {{
            font-style: italic;
        }}
        code, pre {{
            font-family: Courier, monospace;
            background-color: #f8f8f8;
            padding: 2px 4px;
            border-radius: 3px;
        }}
    </style>
    </head>
    <body>
    {source_html}
    </body>
    </html>
    """
    
    # Convert HTML to PDF using pisa
    pisa_status = pisa.CreatePDF(full_html, dest=result_file)
    
    # Return PDF data if successful
    if pisa_status.err:
        raise Exception("PDF conversion failed")
    
    result_file.seek(0)
    return result_file.getvalue()

def markdown_to_pdf(markdown_text):
    """Convert markdown to PDF"""
    # First convert markdown to HTML (without the style tags for xhtml2pdf)
    html = markdown.markdown(markdown_text)
    
    # Then convert HTML to PDF
    return convert_html_to_pdf(html)

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
    st.query_params.clear()

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
    
    # Create a clean and professional preview container
    st.markdown("<h3 style='margin-bottom: 15px; color: #0d47a1;'>📝 Preview</h3>", unsafe_allow_html=True)
    
    # Show enhanced preview
    styled_html = convert_markdown_to_html(st.session_state.current_script)
    st.markdown(styled_html, unsafe_allow_html=True)
    
    # Edit button/expander (hidden by default)
    with st.expander("Edit Script", expanded=False):
        updated_script = st.text_area("Your YouTube Script (editable):", st.session_state.current_script, height=300)
        # Save any manual edits back to the session state
        if updated_script != st.session_state.current_script:
            st.session_state.current_script = updated_script
            st.experimental_rerun()  # Refresh to show updated preview
    
    # Download buttons with improved layout
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # Download as text file
        st.download_button(
            label="📄 Download as Text",
            data=st.session_state.current_script,
            file_name="youtube_script.txt",
            mime="text/plain"
        )
    with col2:
        # Download as PDF with error handling
        try:
            # Generate PDF with styling (keep the existing PDF generation code)
            pdf_data = markdown_to_pdf(st.session_state.current_script)
            
            st.download_button(
                label="📕 Download as PDF",
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
