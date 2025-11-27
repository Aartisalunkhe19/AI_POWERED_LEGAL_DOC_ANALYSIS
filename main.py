import streamlit as st
import yaml
import PyPDF2
import docx
from yaml.loader import SafeLoader
from auth import authenticate, logout
from functions.vectorstore import (
    get_text_chunks, get_vectorstore, 
    get_conversation_chain, handle_userinput
)
from dotenv import load_dotenv

load_dotenv()

# Custom CSS for Modern UI
def set_custom_css():
    st.markdown(
        """
        <style>
        .stApp { font-family: 'Arial', sans-serif; }
        .stButton>button { border-radius: 20px; padding: 10px 20px; font-size: 16px; }
        .stButton>button:hover { background-color: #45a049; }
        .stTextInput>div>div>input { border-radius: 5px; border: 1px solid #ccc; padding: 10px; }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 20px; }
        h2 { color: #34495e; margin-bottom: 15px; }
        .card { background-color: rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
        .stSpinner>div { border-color: #4CAF50; }
        </style>
        """,
        unsafe_allow_html=True,
    )
set_custom_css()

# Extract text from documents
def get_document_text(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    try:
        if file_extension == "pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            return "\n".join([page.extract_text() or "" for page in pdf_reader.pages]).strip()
        elif file_extension == "docx":
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs]).strip()
        elif file_extension == "txt":
            return uploaded_file.getvalue().decode("utf-8").strip()
        else:
            return "❌ Unsupported file format!"
    except Exception as e:
        return f"❌ Error processing file: {e}"

# Main Functionality (Upload and Summarize)
def main_functionality():
    st.title("Document Analysis 📄")
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])
    if st.button("Summarize", key="summarize_button"):
        if uploaded_file is not None:
            with st.spinner("Processing the document..."):
                raw_text = get_document_text(uploaded_file)
                if raw_text.startswith("❌"):
                    st.error(raw_text)
                else:
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    handle_userinput("summarize the document")
                    st.success("✅ Summary generated successfully!")
                    if st.session_state.conversation and st.session_state.chat_history:
                        st.subheader("📄 Summary of the Document")
                        for message in st.session_state.chat_history:
                            st.write(message.content)
        else:
            st.error("❌ Please upload a valid document.")

# Initial Page (Before Login)
def initial_page():
    st.title("AI Powered Document Analysis 📄")
    st.write("Welcome to the AI-powered Document Summarizer.")
    st.write("### Features:")
    st.write("✅ Upload a documents (PDF, DOCX, TXT)")
    st.write("✅ AI-generated summaries for quick insights")
    st.write("✅ Secure login & role-based access control")
    st.write("### Get Started:")
    st.write("Please sign in or create an account to use the tool.")

# Main App Logic
def main():
    authentication_status = authenticate()
    if authentication_status:
        main_functionality()
    else:
        initial_page()

if __name__ == "__main__":
    main()