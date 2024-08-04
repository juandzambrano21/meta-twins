import openai
import numpy as np
import os

class EmbeddingModel:
    """A class for generating and handling text embeddings using OpenAI."""

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def embed(self, text: str) -> np.ndarray:
        """Generates an embedding for the given text using OpenAI's API."""
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-ada-002"  # Specify the embedding model
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculates cosine similarity between two vectors."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
