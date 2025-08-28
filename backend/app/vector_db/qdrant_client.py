from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer
from typing import List, Dict

import os
import dotenv
dotenv.load_dotenv()



class QdrantWrapper:
    
    def __init__(
        self,
        collection_name: str,
        embedding_model:str,
        embedding_dim: int,
        distance: str = "Cosine",
        url: str = "http://localhost:6333",
        
    ):
        if collection_name is None:
            raise ValueError("Collection name must be provided.")
        if embedding_model is None:
            raise ValueError("Embedding model must be provided.")
        if embedding_dim is None:
            raise ValueError("Embedding dimension must be provided.")
        self.collection_name = collection_name
        self.client = QdrantClient(url=url)
        self.embedding_dim = embedding_dim
        self.distance = distance.upper()
        
        self.model = SentenceTransformer(embedding_model) 

        # Create collection if not exists
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.embedding_dim,
                distance=Distance[self.distance]
            )
        )

    def upsert_documents(
        self,
        documents: List[Dict],
        text_fields: List[str],
        metadata_fields: List[str]
    ):
        """
        Upsert documents into Qdrant collection.

        documents: List of dicts containing your data
        text_fields: fields to combine for embeddings (e.g., ['question', 'answer'])
        metadata_fields: fields to store as payload for filtering
        """
        points = []
        i=0
        for doc in documents:
            # Combine text fields to create embedding
            text_to_embed = " ".join(str(doc[f]) for f in text_fields if f in doc)
            vector = self.model.encode(text_to_embed).tolist()

            # Prepare payload from metadata fields
            payload = {k: doc[k] for k in metadata_fields if k in doc}

            points.append({
                "id": i,
                "vector": vector,
                "payload": payload
            })
            i+=1

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

