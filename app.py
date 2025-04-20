import os
import streamlit as st
from docx import Document
import google.generativeai as genai
import io
import markdown
import base64
from weasyprint import HTML
import tempfile

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
    # Convert markdown to HTML with proper styling
    html = markdown.markdown(markdown_text)
    # Add basic styling to make it look better
    styled_html = f"""
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        h1 {{ color: #2c3e50; font-size: 28px; margin-top: 20px; }}
        h2 {{ color: #3498db; font-size: 22px; margin-top: 15px; }}
        h3 {{ font-size: 18px; margin-top: 10px; }}
        p {{ margin: 10px 0; }}
        strong {{ font-weight: bold; }}
        em {{ font-style: italic; }}
        code {{ background-color: #f8f8f8; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f8f8f8; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
    {html}
    """
    return styled_html

def markdown_to_pdf(markdown_text):
    """Convert markdown to PDF using WeasyPrint for accurate rendering"""
    # Convert markdown to HTML with styling
    html_content = convert_markdown_to_html(markdown_text)
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(html_content.encode('utf-8'))
        html_path = f.name
    
    # Convert HTML to PDF using WeasyPrint
    try:
        pdf_bytes = io.BytesIO()
        HTML(html_path).write_pdf(pdf_bytes)
        pdf_bytes.seek(0)
        
        # Clean up the temporary file
        os.unlink(html_path)
        
        return pdf_bytes.getvalue()
    except Exception as e:
        # Clean up the temporary file in case of error
        if os.path.exists(html_path):
            os.unlink(html_path)
        raise e

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
    
    # Show only preview using the styled HTML
    st.subheader("Preview:")
    styled_html = convert_markdown_to_html(st.session_state.current_script)
    st.markdown(styled_html, unsafe_allow_html=True)
    
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
            # Generate PDF with exactly the same styling as the preview
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
