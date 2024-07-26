import unittest
from unittest.mock import Mock, patch

from src.retriever import load_retriever
from src.language_model import load_language_model, generate_text
from src.RAG_pipeline import RAGPipeline
from src.searchAPI import app

from fastapi.testclient import TestClient

class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = load_retriever()

    def test_invoke(self):
        query = "How to use a list comprehension in Python?"
        results = self.retriever.invoke(query)
        self.assertIsNotNone(results)
        self.assertTrue(len(results) > 0)

class TestLanguageModel(unittest.TestCase):
    @patch('src.language_model.AutoTokenizer')
    @patch('src.language_model.AutoModelForCausalLM')
    def test_generate_text(self, mock_model, mock_tokenizer):
        mock_tokenizer_instance = Mock()
        mock_tokenizer_instance.encode_plus.return_value = {
            "input_ids": Mock(),
            "attention_mask": Mock()
        }
        mock_tokenizer_instance.decode.return_value = "This is a test response"
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance

        mock_model_instance = Mock()
        mock_model_instance.generate.return_value = [Mock()]
        mock_model.from_pretrained.return_value = mock_model_instance

        model, tokenizer = load_language_model()
        prompt = "Explain list comprehensions"
        response = generate_text(model, tokenizer, prompt)
        self.assertEqual(response, "This is a test response")

class TestRAGPipeline(unittest.TestCase):
    @patch('src.RAG_pipeline.load_retriever')
    @patch('src.RAG_pipeline.load_language_model')
    @patch('src.RAG_pipeline.pipeline')
    def test_answer_question(self, mock_pipeline, mock_load_lm, mock_load_retriever):
        mock_retriever = Mock()
        mock_retriever.invoke.return_value = [Mock(page_content="Relevant context")]
        mock_load_retriever.return_value = mock_retriever

        mock_model, mock_tokenizer = Mock(), Mock()
        mock_load_lm.return_value = (mock_model, mock_tokenizer)

        mock_generator = Mock()
        mock_generator.return_value = [{'generated_text': 'Answer: Test answer'}]
        mock_pipeline.return_value = mock_generator

        rag_pipeline = RAGPipeline()
        question = "What is a decorator in Python?"
        answer = rag_pipeline.answer_question(question)
        self.assertIn("Test answer", answer)

class TestSearchAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('src.searchAPI.RAGPipeline')
    def test_search_endpoint(self, MockRAGPipeline):
        mock_rag_instance = Mock()
        mock_rag_instance.answer_question.return_value = "API test response"
        MockRAGPipeline.return_value = mock_rag_instance

        with patch('src.searchAPI.rag', mock_rag_instance):
            response = self.client.post("/answer", json={"text": "What is asyncio?"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["answer"], "API test response")

if __name__ == '__main__':
    unittest.main()