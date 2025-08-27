from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class QdrantWrapper:
    def __init__(
        self,
        collection_name: str,
        embedding_dim: int = 768,
        distance: str = "Cosine",
        url: str = "http://localhost:6333"
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(url=url)
        self.embedding_dim = embedding_dim
        self.distance = distance.upper()
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2") 

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
            print(doc)
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
            print(points)
            i+=1

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print("✅ KB and Guides indexed successfully from FastAPI")

