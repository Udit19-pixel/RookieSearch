import time
from src.rag_pipeline import RAGPipeline

def calculate_accuracy(predictions, ground_truth):
    correct = sum(1 for p, gt in zip(predictions, ground_truth) if p == gt)
    return correct / len(predictions)

def measure_response_time(pipeline, questions):
    start_time = time.time()
    for question in questions:
        pipeline.answer_question(question)
    end_time = time.time()
    return (end_time - start_time) / len(questions)

def evaluate_relevance(pipeline, questions, expected_keywords):
    relevance_scores = []
    for question, keywords in zip(questions, expected_keywords):
        answer = pipeline.answer_question(question)
        relevance = sum(1 for keyword in keywords if keyword.lower() in answer.lower())
        relevance_scores.append(relevance / len(keywords))
    return sum(relevance_scores) / len(relevance_scores)

def main():
    pipeline = RAGPipeline()
    
    # Sample evaluation data
    questions = [
        "What is a list comprehension in Python?",
        "How do you define a decorator in Python?",
        "Explain the difference between a list and a tuple."
    ]
    ground_truth = [
        "A list comprehension is a concise way to create lists in Python.",
        "A decorator is a function that modifies another function.",
        "Lists are mutable, while tuples are immutable."
    ]
    expected_keywords = [
        ["list", "comprehension", "concise", "create"],
        ["decorator", "function", "modifies"],
        ["list", "tuple", "mutable", "immutable"]
    ]
    
    # Run evaluations
    predictions = [pipeline.answer_question(q) for q in questions]
    accuracy = calculate_accuracy(predictions, ground_truth)
    avg_response_time = measure_response_time(pipeline, questions)
    relevance = evaluate_relevance(pipeline, questions, expected_keywords)
    
    # Log results
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Average Response Time: {avg_response_time:.2f} seconds")
    print(f"Relevance Score: {relevance:.2f}")

if __name__ == "__main__":
    main()