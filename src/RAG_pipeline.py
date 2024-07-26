from retriever import load_retriever
from language_model import load_language_model
from transformers import pipeline

class RAGPipeline:
    def __init__(self):
        self.retriever = load_retriever()
        self.model, self.tokenizer = load_language_model()
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def answer_question(self, question, max_new_tokens=200):
        # Retrieve relevant documents
        docs = self.retriever.invoke(question)
        context = " ".join([doc.page_content for doc in docs[:3]])  # Use top 3 documents

        # Generate answer
        prompt = f"""Based on the following context, please provide a clear, accurate, and concise answer to the question. If the context doesn't contain relevant information, say so.

Context: {context}

Question: {question}

Answer:"""

        response = self.generator(prompt, max_new_tokens=max_new_tokens, num_return_sequences=1, temperature=0.7)[0]['generated_text']

        # Extract the answer part
        answer = response.split("Answer:")[-1].strip()

        # Basic quality check
        if len(answer.split()) < 10 or len(answer.split()) > 100:
            answer += "\n\n\nNote: This answer may be incomplete or require further clarification."

        return answer

# Test the RAG pipeline
if __name__ == "__main__":
    rag = RAGPipeline()
    question = "What is Python?"
    answer = rag.answer_question(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")