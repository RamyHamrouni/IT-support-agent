import requests
from app.vector_db.qdrant_client import QdrantWrapper
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from app.utils.yaml_loader import load_yaml


async def index_documents(app: FastAPI) -> list[str]:
    load_dotenv()
    DB_URL = os.getenv("DB_URL")
    print(f"Fetching data from {DB_URL}")
    try:
        resp = requests.get(f"{DB_URL}/kb")
        resp.raise_for_status()
        kb_data = resp.json()
        print(f"Fetched {len(kb_data)} Knowledge Database entries")
    except requests.RequestException as e:
        print(f"Error fetching KB data: {e}")
        return []

    # --- Fetch Guides ---
    try:
        resp = requests.get(f"{DB_URL}/guide")
        resp.raise_for_status()
        guide_data = resp.json()
        print(f"Fetched {len(guide_data)} Guide entries")
    except requests.RequestException as e:
        print(f"Error fetching Guide data: {e}")
        return []
    embedding = load_yaml("embedding.yaml")
        
    kb_indexer = QdrantWrapper(collection_name="kb_collection",
                               embedding_model=embedding.get('embedding_model').get('default_model'), 
                               embedding_dim=embedding.get("embedding_model", {}).get("params", {}).get("embedding_dim", 768))
    try:
        kb_indexer.upsert_documents(
            documents=[{k: v for k, v in d.items() if k != "id"} for d in kb_data],
            text_fields=["question", "answer"],
            metadata_fields=["category", "issue_code"]
        )
        print("✅ Knowledge Database indexed successfully")
    except Exception as e:
        print(f"Error indexing KB data: {e}")
        return []
        

    # --- Index Guides in Qdrant ---        
    guide_indexer = QdrantWrapper(collection_name="guide_collection", embedding_model=embedding.get('embedding_model').get('default_model'), 
                               embedding_dim=embedding.get("embedding_model", {}).get("params", {}).get("embedding_dim", 768))
    try:
        guide_indexer.upsert_documents(
            documents=[{k: v for k, v in d.items() if k != "id"} for d in guide_data],
            text_fields=["issue", "diagnostic_questions", "troubleshooting_steps"],
            metadata_fields=["category", "issue_code"]
        )
        print("✅ Guides indexed successfully ")
    except Exception as e:
        print(f"Error indexing Guide data: {e}")
        return []
    # --- Return combined unique categories ---
    kb_categories = {item["category"] for item in kb_data}
    guide_categories = {item["category"] for item in guide_data}
    all_categories = sorted(kb_categories.union(guide_categories))
    return all_categories