import json
import os
import time

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings

import torch
from tqdm import tqdm
import gc

load_dotenv()

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        if torch.cuda.is_available():
            self.model = self.model.to('cuda')

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, text):
        return self.model.encode(text)

    def __call__(self, text):
        if isinstance(text, list):
            return self.embed_documents(text)
        else:
            return self.embed_query(text)

def count_items_in_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return len(data)

def load_data_generator(file_path, batch_size=1000):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]

def process_chunk(item, text_splitter):
    content = item.get('content', '')
    if not content:
        return []
    
    chunks = text_splitter.split_text(content)
    documents = []
    for chunk in chunks:
        metadata = {
            'source': item.get('source', ''),
            'timestamp': item.get('timestamp', '')
        }
        for key, value in item.items():
            if key not in ['content', 'source', 'timestamp']:
                metadata[key] = value
        documents.append({
            'content': chunk,
            'metadata': metadata
        })
    return documents

def create_vector_store(data_generator, embedding_model):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    vector_store = None
    
    batch_times = []
    
    for batch in tqdm(data_generator, desc="Processing batches"):
        start_time = time.time()
        
        documents = []
        for item in batch:
            documents.extend(process_chunk(item, text_splitter))
        
        texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
       
        if vector_store is None:
            vector_store = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)
        else:
            vector_store.add_texts(texts, metadatas=metadatas)
        
        del documents, texts, metadatas
        gc.collect()
        
        end_time = time.time()
        batch_times.append(end_time - start_time)
    
    avg_time_per_batch = sum(batch_times) / len(batch_times)
    total_time_estimate = avg_time_per_batch * len(batch_times)
    
    print(f"Average time per batch: {avg_time_per_batch} seconds")
    print(f"Estimated total time: {total_time_estimate / 60} minutes")
    
    return vector_store

def main():
    file_path = 'D:\Python\RookieSearch\RookieSearch\src\preprocessing\preprocessed_python_docs.json'
    total_items = count_items_in_json(file_path)
    batch_size = 1000
    num_batches = (total_items + batch_size - 1) // batch_size  # This ensures we round up to the next integer

    print(f"Total items: {total_items}")
    print(f"Batch size: {batch_size}")
    print(f"Number of batches: {num_batches}")

    data_generator = load_data_generator(file_path, batch_size=batch_size)
    embedding_model = SentenceTransformerEmbeddings()
    vector_store = create_vector_store(data_generator, embedding_model)
   
    # Save the vector store
    vector_store.save_local("faiss_index")

if __name__ == "__main__":
    main()