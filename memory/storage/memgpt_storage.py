import json
import numpy as np
from memory.embeddings import EmbeddingModel
from memory.messages import RecallMemory
from memory.persistence import PersistenceManager
from memory.storage.interface import Storage
from memory.base_memory import BaseMemory
from memory.executor import FunctionExecutor
from utils.logger import logger
from typing import Any, Dict, List

class MemGPTStorage(Storage):
    """Storage implementation using MemGPT architecture."""

    def __init__(self, persona: str, human: str, persistence_manager: PersistenceManager):
        super().__init__()
        self.embedding_model = EmbeddingModel()
        self.core_memory = BaseMemory()
        self.archival_memory = []
        self.recall_memory = RecallMemory()
        self.persistence_manager = persistence_manager
        self.function_executor = FunctionExecutor(self.core_memory, self.archival_memory, self.recall_memory)
        self.persona = persona
        self.human = human

        # Load memory data at initialization
        self.load_memory()

    def load_memory(self) -> None:
        """Load memory data using PersistenceManager."""
        logger.debug("Loading memory data from persistent storage")
        
        try:
            # Load core, archival, and recall memories
            self.persistence_manager.load("data/core_memory.json")
            self.persistence_manager.load("data/archival_memory.json")
            self.persistence_manager.load("data/recall_memory.json")
            self.persistence_manager.load("data/short_term_memory.json")

            # Update local memory attributes
            self.core_memory = self.persistence_manager.core_memory
            self.archival_memory = self.persistence_manager.archival_memory
            self.recall_memory = self.persistence_manager.recall_memory

            logger.info("Memory loaded successfully.")

        except Exception as e:
            logger.error(f"Error loading memory data: {e}")
            # Initialize empty memories if loading fails
            self.core_memory = BaseMemory()
            self.archival_memory = []
            self.recall_memory = RecallMemory()

    def save_memory(self) -> None:
        """Save memory data using PersistenceManager."""
        logger.debug("Saving memory data to persistent storage")
        
        try:
            # Persist each memory component
            self.persistence_manager.save("data/core_memory.json")
            self.persistence_manager.save("data/archival_memory.json")
            self.persistence_manager.save("data/recall_memory.json")
            self.persistence_manager.save("data/short_term_memory.json")
            logger.info("Memory persisted successfully.")
        except Exception as e:
            logger.error(f"Error persisting memory: {e}")

    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        """Save a value with associated metadata."""
        embedding = self.embedding_model.embed(value)
        entry = {
            "value": value,
            "metadata": metadata,
            "embedding": embedding.tolist()
        }
        self.storage.append(entry)
        logger.debug(f"Saved entry: {entry}")

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search for entries containing the query using embeddings for semantic similarity."""
        query_embedding = self.embedding_model.embed(query)
        results = []
        
        for entry in self.storage:
            entry_embedding = np.array(entry['embedding'], dtype=np.float32)
            similarity_score = self.embedding_model.similarity(query_embedding, entry_embedding)
            if similarity_score > 0.5:  # Assuming a threshold for semantic match
                results.append({
                    "value": entry['value'],
                    "metadata": entry['metadata'],
                    "score": similarity_score
                })
        
        # Sort results based on similarity scores
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        return sorted_results

    def reset(self) -> None:
        """Reset the storage by clearing all entries."""
        self.storage = []
        self.current_id = 0
        logger.info("Storage has been reset.")

    def append(self, module_name: str, new_content: str) -> None:
        """Append new content to a specific module."""
        for entry in self.storage:
            if entry['metadata'].get('module_name') == module_name:
                entry['value'] += new_content
                logger.debug(f"Appended new content to module '{module_name}'.")
                return
        raise ValueError(f"Module '{module_name}' not found.")

    def replace(self, module_name: str, old_content: str, new_content: str) -> None:
        """Replace old content with new content in a specific module."""
        for entry in self.storage:
            if entry['metadata'].get('module_name') == module_name:
                if old_content in entry['value']:
                    entry['value'] = entry['value'].replace(old_content, new_content)
                    logger.debug(f"Replaced content in module '{module_name}'.")
                else:
                    raise ValueError(f"Old content not found in module '{module_name}'.")
                return
        raise ValueError(f"Module '{module_name}' not found.")

    def persist_memory(self):
        """Persist memory data to files."""
        self.save_memory()
