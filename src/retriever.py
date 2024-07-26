from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def load_retriever(index_path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store.as_retriever()

# Test the retriever
if __name__ == "__main__":
    retriever = load_retriever()
    query = "How do I use decorators in Python?"
    docs = retriever.invoke(query)
    print(f"Found {len(docs)} relevant documents")
    for doc in docs[:2]:  # Print first 2 documents
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")
        print("---")