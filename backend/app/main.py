import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.chat import ChatRequest, ChatResponse

from contextlib import asynccontextmanager
from app.services.indexer import index_documents
from app.services.chat_service import process_chat
from fastapi import Request



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: index documents
    all_categories = await index_documents(app=app)  # ✅ await the coroutine
    app.state.all_categories = all_categories
    yield
    
    
    
app = FastAPI(title="IT-support-Backend", lifespan=lifespan)


allowed_origins = (os.getenv("ALLOWED_ORIGINS") or "http://localhost:8501").split(",")
app.add_middleware(
CORSMiddleware,
allow_origins=[o.strip() for o in allowed_origins],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)




@app.get("/")
async def root():
    return {"message": "Hello from HF Chat Backend!"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):
    """
    Chat endpoint:
    - Fetches the global categories from app.state
    - Builds the prompt
    - Calls the LLM
    """
    categories = request.app.state.all_categories  # global categories

    # Pass categories to service, which will handle prompts & tools
    response = await process_chat(req, categories)
    return response
if __name__ == "__main__":
    import uvicorn

    # Run on localhost:8500
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
