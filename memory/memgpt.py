import os
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from memory.entity_memory import EntityMemory
from memory.embeddings import EmbeddingModel
from memory.persistence import PersistenceManager
from memory.contextual_memory import ContextualMemory
from memory.base_memory import BaseMemory
from memory.messages import RecallMemory
from memory.executor import FunctionExecutor
from memory.storage.memgpt_storage import MemGPTStorage
from utils.logger import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MemGPT:
    """Main MemGPT class integrating memory management and execution."""

    def __init__(self, persona: str, human: str, embedding_model: EmbeddingModel):
        # Initialize memory components with default structures if loading fails
        self.core_memory = BaseMemory()
        self.archival_memory = []
        self.recall_memory = RecallMemory()
        self.persistence_manager = PersistenceManager(self.core_memory, self.archival_memory, self.recall_memory)

        # Initialize short-term, long-term, and entity memory
        self.short_term_memory = ShortTermMemory(persona, human, self.persistence_manager)
        self.long_term_memory = LongTermMemory(persona, human, self.persistence_manager)
        self.entity_memory = EntityMemory(persona, human, self.persistence_manager)

        # Contextual memory combines all memory types
        self.contextual_memory = ContextualMemory(self.short_term_memory, self.long_term_memory, self.entity_memory)

        # Initialize function executor
        self.function_executor = FunctionExecutor(self.core_memory, self.archival_memory, self.recall_memory)

        # Initialize storage
        self.storage = MemGPTStorage(persona, human, self.persistence_manager)

        # Load all memory states
        self.load_all_memories()  # Ensure this is called during initialization

    def load_all_memories(self):
        """Loads all memory states from respective files."""
        
        # Logging for memory loading
        logger.info("Loading all memory states")
        
        self.short_term_memory.load_memory()
        self.long_term_memory.load_memory()
        self.entity_memory.load_memory()
        self.storage.load_memory()

    def save_all_memories(self):
        """Saves all memory states."""
        
        # Logging for memory saving
        logger.info("Saving all memory states")
        
        self.short_term_memory.persist_memory()
        self.long_term_memory.persist_memory()
        self.entity_memory.persist_memory()
        self.storage.persist_memory()
