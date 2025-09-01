from fastapi import FastAPI
from app.db.qdrant_client import QdrantWrapper
from app.utils.yaml_loader import load_yaml
from app.db.database_client import fetch_kb_data, fetch_guide_data
from typing import List, Dict


def index_collection(
    collection_name: str,
    data: List[Dict],
    text_fields: List[str],
    payload_fields: List[str],
    embedding: dict
):
    """Helper function to index a single collection in Qdrant."""
    indexer = QdrantWrapper(
        collection_name=collection_name,
        embedding_model=embedding.get('embedding_model', {}).get('default_model'),
        embedding_dim=embedding.get("embedding_model", {}).get("params", {}).get("embedding_dim", 768)
    )
    try:
        indexer.upsert_documents(
            documents=[{k: v for k, v in d.items()} for d in data],
            text_fields=text_fields,
            payload_fields=payload_fields
        )
        print(f"✅ {collection_name} indexed successfully")
    except Exception as e:
        print(f"Error indexing {collection_name}: {e}")
        return False
    return True


async def index_documents(app: FastAPI) -> List[str]:
    kb_data = fetch_kb_data()
    guide_data = fetch_guide_data()

    if not kb_data and not guide_data:
        return []

    embedding = load_yaml("embedding.yaml")

    # Index KB
    if kb_data:
        index_collection(
            collection_name="kb_collection",
            data=kb_data,
            text_fields=["question", "answer"],
            payload_fields=["category", "issue_code", "answer", "question"],
            embedding=embedding
        )

    # Index Guides
    if guide_data:
        index_collection(
            collection_name="guide_collection",
            data=guide_data,
            text_fields=["issue", "resolution_steps"],
            payload_fields=[
                "category",
                "issue_code",
                "issue",
                "troubleshooting_steps",
                "quick_fixes",
                "escalation_criteria",
                "diagnostic_questions",
            ],
            embedding=embedding
        )

    # Return combined unique categories
    kb_categories = {item["category"] for item in kb_data}
    guide_categories = {item["category"] for item in guide_data}
    all_categories = sorted(kb_categories.union(guide_categories))
    return all_categories
