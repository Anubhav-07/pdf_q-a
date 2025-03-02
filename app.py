import streamlit as st
import os
from pdf_processor import process_pdf, answer_question
import time

# Set page config
st.set_page_config(page_title="📄 PDF Q&A System", page_icon="📄", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("📄 PDF Q&A System")
st.write("🔍 Ask questions and get instant answers from your PDFs!")

# Sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("1. Upload a PDF file.")
    st.write("2. Ask a question about the document.")
    st.write("3. Get instant answers!")
    st.write("4. Enjoy!")

# File uploader
st.write("### Upload a PDF document to get started:")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save file temporarily
    pdf_path = os.path.join("uploads", uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process PDF
    with st.spinner("Processing PDF..."):
        process_pdf(pdf_path)
        st.success("PDF processed successfully!")

    # Ask questions
    st.write("### Ask a question about the document:")
    query = st.text_input("Enter your question:", placeholder="e.g., What is the main topic?")

    if st.button("Get Answer"):
        if query:
            with st.spinner("Generating answer..."):
                try:
                    answer = answer_question(query, k=5)
                    st.markdown(f"**Answer:** {answer}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question.")
else:
    st.warning("Please upload a PDF file.")
