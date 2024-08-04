# memory/entity_memory.py

from memory.storage.memgpt_storage import MemGPTStorage
from memory.persistence import PersistenceManager

class EntityMemoryItem:
    """Represents an item in entity memory."""
    
    def __init__(
        self,
        name: str,
        type: str,
        description: str,
        relationships: str,
    ):
        self.name = name
        self.type = type
        self.description = description
        self.metadata = {"relationships": relationships}


class EntityMemory:
    """
    EntityMemory class for managing structured information about entities and their relationships.
    """

    def __init__(self, persona: str, human: str, persistence_manager: PersistenceManager):
        self.persistence_manager = persistence_manager
        self.storage = MemGPTStorage(persona, human, persistence_manager)
        self.file_name = 'data/entity_memory.json'
        self.load_memory()

    def save(self, item: EntityMemoryItem) -> None:
        """Saves an entity item into the storage."""
        data = f"{item.name}({item.type}): {item.description}"
        self.storage.save(data, item.metadata)
        self.persist_memory()

    def search(self, query: str):
        return self.storage.search(query=query)

    def reset(self) -> None:
        try:
            self.storage.reset()
            self.persist_memory()
        except Exception as e:
            raise Exception(f"An error occurred while resetting the entity memory: {e}")

    def persist_memory(self) -> None:
        self.storage.persistence_manager.save(self.file_name)

    def load_memory(self) -> None:
        self.storage.persistence_manager.load(self.file_name)
