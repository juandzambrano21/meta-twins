# memory/long_term_memory.py

from typing import Any, Dict, Optional, Union
from memory.storage.memgpt_storage import MemGPTStorage
from memory.persistence import PersistenceManager

class LongTermMemoryItem:
    def __init__(self, agent: str, task: str, expected_output: str, datetime: str, quality: Optional[Union[int, float]] = None, metadata: Optional[Dict[str, Any]] = None):
        self.task = task
        self.agent = agent
        self.quality = quality
        self.datetime = datetime
        self.expected_output = expected_output
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        """Converts LongTermMemoryItem to a dictionary."""
        return {
            "task": self.task,
            "agent": self.agent,
            "quality": self.quality,
            "datetime": self.datetime,
            "expected_output": self.expected_output,
            "metadata": self.metadata
        }

class LongTermMemory:
    """
    LongTermMemory class for managing persistent data related to execution and performance across sessions.
    """

    def __init__(self, persona: str, human: str, persistence_manager: PersistenceManager):
        self.persistence_manager = persistence_manager
        self.storage = MemGPTStorage(persona, human, persistence_manager)
        self.file_name = 'data/long_term_memory.json'
        self.load_memory()

    def save(self, item: LongTermMemoryItem) -> None:
        metadata = item.metadata
        metadata.update({"agent": item.agent, "expected_output": item.expected_output})
        self.storage.save(value=item.task, metadata=metadata)
        self.persist_memory()

    def search(self, task: str, latest_n: int = 3) -> Dict[str, Any]:
        return self.storage.search(task)

    def reset(self) -> None:
        self.storage.reset()
        self.persist_memory()

    def persist_memory(self) -> None:
        self.storage.persistence_manager.save(self.file_name)

    def load_memory(self) -> None:
        self.storage.persistence_manager.load(self.file_name)
