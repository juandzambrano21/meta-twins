# memory/short_term_memory.py

from typing import Any, Optional, Dict
from memory.storage.memgpt_storage import MemGPTStorage
from memory.persistence import PersistenceManager
import os 

class ShortTermMemoryItem:
    """Represents an item in the short-term memory."""

    def __init__(
        self,
        data: Any,
        agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.data = data
        self.agent = agent
        self.metadata = metadata if metadata is not None else {}


class ShortTermMemory:
    """
    ShortTermMemory class for managing transient data related to immediate tasks
    and interactions.
    """

    def __init__(self, persona: str, human: str, persistence_manager: PersistenceManager):
        self.storage = MemGPTStorage(persona, human, persistence_manager)
        self.file_name = 'data/short_term_memory.json'
        self.load_memory()

    def save(
        self,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None,
        agent: Optional[str] = None,
    ) -> None:
        item = ShortTermMemoryItem(data=value, metadata=metadata, agent=agent)
        self.storage.save(value=item.data, metadata=item.metadata)
        self.persist_memory()

    def search(self, query: str):
        return self.storage.search(query=query)

    def reset(self) -> None:
        try:
            self.storage.reset()
            self.persist_memory()
        except Exception as e:
            raise Exception(f"An error occurred while resetting the short-term memory: {e}")

    def persist_memory(self) -> None:
        self.storage.persistence_manager.save(os.path.join("data", self.file_name))

    def load_memory(self) -> None:
        self.storage.persistence_manager.load(os.path.join("data", self.file_name))

