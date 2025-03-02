from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load QA model (try a different model if needed)
qa_model = pipeline("question-answering", model="deepset/bert-large-uncased-whole-word-masking-squad2")

# Function to process and index PDF
def process_pdf(pdf_path):
    # Extract text from PDF
    pdfreader = PdfReader(pdf_path)
    raw_text = ''
    
    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    # Split and chunk the text
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800, 
        chunk_overlap=200,  
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    # Create FAISS Vector Store
    document_search = FAISS.from_texts(texts, embedding_model)
    document_search.save_local("faiss_index")

# Function to answer questions using FAISS & QA model
def answer_question(query, k=3):  
    # Load the FAISS Index
    document_search = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
    
    # Search FAISS for relevant documents
    results = document_search.similarity_search(query, k=k)
    
    if not results:
        return "No relevant content found in the PDF."
    
    # Combine the top k chunks for context
    context = " ".join([result.page_content for result in results])
    
    # Run the question through the QA model
    response = qa_model(question=query, context=context)
    return response["answer"]