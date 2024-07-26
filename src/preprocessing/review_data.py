import json
from collections import Counter
import statistics

def load_preprocessed_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_data(data):
    total_chunks = len(data)
    chunk_lengths = [len(item['content']) for item in data]
    unique_titles = len(set(item['title'] for item in data))
    unique_urls = len(set(item['url'] for item in data))

    # Analyze content
    word_counts = [len(item['content'].split()) for item in data]
    total_words = sum(word_counts)

    # Get most common titles
    title_counter = Counter(item['title'] for item in data)
    most_common_titles = title_counter.most_common(5)

    return {
        'total_chunks': total_chunks,
        'unique_titles': unique_titles,
        'unique_urls': unique_urls,
        'total_words': total_words,
        'avg_chunk_length': statistics.mean(chunk_lengths),
        'min_chunk_length': min(chunk_lengths),
        'max_chunk_length': max(chunk_lengths),
        'avg_words_per_chunk': statistics.mean(word_counts),
        'min_words_per_chunk': min(word_counts),
        'max_words_per_chunk': max(word_counts),
        'most_common_titles': most_common_titles
    }

def print_analysis(analysis):
    print("Data Analysis:")
    print(f"Total chunks: {analysis['total_chunks']}")
    print(f"Unique titles: {analysis['unique_titles']}")
    print(f"Unique URLs: {analysis['unique_urls']}")
    print(f"Total words: {analysis['total_words']}")
    print(f"Average chunk length: {analysis['avg_chunk_length']:.2f} characters")
    print(f"Min chunk length: {analysis['min_chunk_length']} characters")
    print(f"Max chunk length: {analysis['max_chunk_length']} characters")
    print(f"Average words per chunk: {analysis['avg_words_per_chunk']:.2f}")
    print(f"Min words per chunk: {analysis['min_words_per_chunk']}")
    print(f"Max words per chunk: {analysis['max_words_per_chunk']}")
    print("\nMost common titles:")
    for title, count in analysis['most_common_titles']:
        print(f"  - {title}: {count} chunks")

def print_sample_chunks(data, num_samples=5):
    print(f"\nSample chunks (showing {num_samples}):")
    for i, chunk in enumerate(data[:num_samples], 1):
        print(f"\nChunk {i}:")
        print(f"Title: {chunk['title']}")
        print(f"URL: {chunk['url']}")
        print(f"Content preview: {chunk['content'][:100]}...")

if __name__ == "__main__":
    input_file = "preprocessed_python_docs.json"
    
    print("Loading preprocessed data...")
    preprocessed_data = load_preprocessed_data(input_file)

    print("Analyzing data...")
    analysis_results = analyze_data(preprocessed_data)

    print_analysis(analysis_results)
    print_sample_chunks(preprocessed_data)

    print("\nData review complete.")