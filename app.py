import streamlit as st
import os
from pdf_processor import process_pdf, answer_question  # Import necessary functions
import asyncio

# Ensure an event loop exists
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Title
st.title("📄 PDF Q&A System")

# Ensure 'uploads' directory exists
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# 🔹 Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # 🔹 Save file temporarily
    pdf_path = os.path.join("uploads", uploaded_file.name)
    
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 🔹 Process PDF & Build FAISS Index
    with st.spinner("Processing PDF and building FAISS index..."):
        process_pdf(pdf_path)
    st.success("✅ PDF processed and FAISS index saved!")

    # 🔹 Let user ask questions after processing
    query = st.text_input("Ask a question about the document:")
    
    # 🔹 Add a button to trigger the answer generation
    if st.button("Get Answer"):
        if query:
            with st.spinner("Generating answer..."):
                try:
                    answer = answer_question(query)  # Get answer using the QA system
                    st.write(f"**Answer:** {answer}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question.")