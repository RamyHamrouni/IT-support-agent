from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams, Filter, models, PayloadSchemaType
from sentence_transformers import SentenceTransformer
from typing import List, Dict

import dotenv
dotenv.load_dotenv()
import os

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


class QdrantWrapper:
    
    def __init__(
        self,
        collection_name: str,
        embedding_model: str,
        embedding_dim: int,
        distance: str = "Cosine",
        url: str = QDRANT_URL,
    ):
        if collection_name is None:
            raise ValueError("Collection name must be provided.")
        if embedding_model is None:
            raise ValueError("Embedding model must be provided.")
        if embedding_dim is None:
            raise ValueError("Embedding dimension must be provided.")
            
        self.collection_name = collection_name
        self.client = QdrantClient(url=url, api_key=QDRANT_API_KEY)
        self.embedding_dim = embedding_dim
        self.distance = distance.upper()
        
        self.model = SentenceTransformer(embedding_model) 

        # Create collection if not exists
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance[self.distance]
                )
            )

    # NEW helper
    def ensure_index(self, field_name: str):
        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name=field_name,
                field_schema=PayloadSchemaType.KEYWORD
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise

    def upsert_documents(
        self,
        documents: List[Dict],
        text_fields: List[str],
        payload_fields: List[str]
    ):
        points = []
        i = 0
        for doc in documents:
            # Combine text fields to create embedding
            text_to_embed = " ".join(str(doc[f]) for f in text_fields if f in doc)
            vector = self.model.encode(text_to_embed).tolist()

            # Prepare payload from metadata fields
            payload = {k: doc[k] for k in payload_fields if k in doc}

            points.append({
                "id": i,
                "vector": vector,
                "payload": payload
            })
            i += 1

        for field in payload_fields:
            self.ensure_index(field)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def query(self, query: str, metadata_key: str, metadata_value: str, max_results: int):
        self.ensure_index(metadata_key)

        query_vector = self.model.encode(query)
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=max_results,
            query_filter=Filter(
                must=[
                    models.FieldCondition(
                        key=metadata_key,
                        match=models.MatchValue(value=metadata_value)
                    )
                ]
            )
        )
        return hits
