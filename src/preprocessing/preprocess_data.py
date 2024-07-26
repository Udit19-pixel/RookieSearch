import json
import re
from typing import List, Dict

def load_data(file_path: str) -> List[Dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text: str) -> str:
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters (keeping alphanumeric, spaces, and basic punctuation)
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!]', '', text)
    return text

def split_into_chunks(text: str, max_chunk_size: int = 1000) -> List[str]:
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk)) + len(word) > max_chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def preprocess_data(data: List[Dict], max_chunk_size: int = 1000) -> List[Dict]:
    preprocessed_data = []

    for item in data:
        cleaned_content = clean_text(item['content'])
        chunks = split_into_chunks(cleaned_content, max_chunk_size)

        for i, chunk in enumerate(chunks):
            preprocessed_item = {
                'title': item['title'],
                'content': chunk,
                'url': item['url'],
                'chunk_id': f"{item['title']}_{i}",
                'source': 'Python Documentation'
            }
            preprocessed_data.append(preprocessed_item)

    return preprocessed_data

def save_preprocessed_data(data: List[Dict], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_file = "python_docs_data_final.json"
    output_file = "preprocessed_python_docs.json"

    print("Loading data...")
    raw_data = load_data(input_file)

    print("Preprocessing data...")
    preprocessed_data = preprocess_data(raw_data)

    print("Saving preprocessed data...")
    save_preprocessed_data(preprocessed_data, output_file)

    print(f"Preprocessing complete. {len(preprocessed_data)} chunks created.")
    print(f"Preprocessed data saved to {output_file}")