from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from RAG_pipeline import RAGPipeline
from monitoring import run_scheduled_tasks

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

rag = RAGPipeline()

class Question(BaseModel):
    text: str

@app.post("/answer")
async def answer_question(question: Question):
    answer = rag.answer_question(question.text)
    return {"answer": answer}

@app.get("/")
async def root():
    return {"message": "Welcome to RookieSearch API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from RAG_pipeline import RAGPipeline