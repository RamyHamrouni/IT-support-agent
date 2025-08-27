import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, ChatResponse
from .llm.hf_client import HFClient

import requests
from dotenv import load_dotenv
from .vector_db.qdrant_client import QdrantWrapper
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: index documents
    index_documents(app=app)
    yield
    # Shutdown: you can add cleanup code here if needed
app = FastAPI(title="IT-support-Backend", lifespan=lifespan)


allowed_origins = (os.getenv("ALLOWED_ORIGINS") or "http://localhost:8501").split(",")
app.add_middleware(
CORSMiddleware,
allow_origins=[o.strip() for o in allowed_origins],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


client = HFClient()
DEFAULT_MODEL = os.getenv("HF_DEFAULT_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")


SYSTEM_PROMPT = (
"You are a helpful, concise assistant. Answer clearly and avoid excessive verbosity."
)

@asynccontextmanager
def index_documents(app: FastAPI) -> None:
    load_dotenv()

    
    DB_URL = os.getenv("DB_URL")
    resp = requests.get(f"{DB_URL}/kb")
    resp.raise_for_status()
    kb_data = resp.json()

    # --- Fetch Guides ---
    resp = requests.get(f"{DB_URL}/guide")
    resp.raise_for_status()
    guide_data = resp.json()
    print(guide_data)
    kb_indexer = QdrantWrapper(collection_name="kb_collection", embedding_dim=768)
    kb_indexer.upsert_documents(
        documents=[{k: v for k, v in d.items() if k != "id"} for d in kb_data],
        text_fields=["question", "answer"],
        metadata_fields=["category", "issue_code", "tags", "source_url"]
    )

    # --- Index Guides in Qdrant ---
    guide_indexer = QdrantWrapper(collection_name="guide_collection", embedding_dim=768)
    guide_indexer.upsert_documents(
        documents=[{k: v for k, v in d.items() if k != "id"} for d in guide_data],
        text_fields=["issue", "diagnostic_questions", "troubleshooting_steps"],
        metadata_fields=["category", "issue_code", "quick_fixes", "escalation_criteria", "kb_links"]
    )
    global all_categories
    kb_categories = {item["category"] for item in kb_data}
    guide_categories = {item["category"] for item in guide_data}
    all_categories = sorted(kb_categories.union(guide_categories))


    
def build_prompt(messages: list[dict[str, str]]) -> str:
    """
    Model-agnostic prompt formatting with workflow guidance for Level-1 IT support.
    """
    parts = []
    system = SYSTEM_PROMPT
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            system = content  # last system message wins
        else:
            parts.append(f"{role.upper()}: {content}")
    convo = "\n".join(parts)

    # Add Level-1 IT workflow instructions
    workflow_instructions = f"""Workflow Instructions (step-by-step):
First, check if the user's issue matches any of the following categories:
Available Categories: {', '.join(all_categories)}
If the issue does NOT match any category, RESPOND with a polite message indicating that the issue is out of scope and suggest contacting Level-2 support directly.
If the issue falls under one of these categories, proceed with the following steps.
1. ONLY query the internal knowledge base first.
   - If you find a direct answer, RETURN it immediately.
2. If no answer is found in the internal knowledge base, THEN query the issue guide.
   - Only return solutions from the issue guide if the knowledge base had no answer.
3. If the issue is still unresolved, ASK the user whether they want to create a ticket or continue clarifying.
   - Do NOT query any other source until the user responds.
4. If the user confirms ticket creation, CALL the ticket creation tool with appropriate arguments.
   - Otherwise, continue helping the user clarify their issue.
5. Always provide responses in a clear, concise manner, and never skip a step.
"""
    return f"<SYSTEM>\n{system}\n{workflow_instructions}\n</SYSTEM>\n\n{convo}\nASSISTANT:"



@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Hello from HF Chat Backend!"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = req.model or DEFAULT_MODEL
    prompt = build_prompt([m.dict() for m in req.messages])
    params = {
        "max_new_tokens": req.max_new_tokens,
        "temperature": req.temperature,
        "top_p": req.top_p,
        "return_full_text": False,
    }
    tools = [
            {
                "type": "function",
                "function": {
                    "name": "query_knowledge_base",
                    "description": "Query the internal knowledge base for relevant articles or solutions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query for the knowledge base"},
                            "max_results": {"type": "integer", "description": "Maximum number of results to return"},
                            "type_issue": {"type": "string", "description": "Type of the issue", "enum": all_categories}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_issue_guide",
                    "description": "Search FAQs to provide immediate answers to common issues.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query for FAQs"},
                            "max_results": {"type": "integer", "description": "Maximum number of FAQ answers to return"},
                            "type_issue": {"type": "string", "description": "Type of the issue", "enum": all_categories}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "manage_ticket",
                    "description": "Create or update a ticket with the given state.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "issue_description": {"type": "string", "description": "Description of the user's issue"},
                            "action": {"type": "string", "enum": ["open", "close"], "description": "Open or close the ticket"},
                            "ticket_id": {"type": "string", "description": "Ticket ID if updating an existing ticket"}
                        },
                        "required": ["issue_description", "action"]
                    }
                }
            }
        ]
    text = client.generate(model=model, prompt=prompt, params=params,tools=tools)

    if text.startswith(prompt):
        text = text[len(prompt):].lstrip()

    return ChatResponse(reply=text)
if __name__ == "__main__":
    import uvicorn

    # Run on localhost:8500
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
