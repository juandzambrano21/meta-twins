import json
import numpy as np
import ipdb  # Import ipdb for debugging
from utils.logger import logger
from memory.base_memory import BaseMemory
from memory.messages import RecallMemory, Message
from typing import List, Tuple

class PersistenceManager:
    """Manages the persistence of core, archival, and recall memory."""

    def __init__(self, core_memory: BaseMemory, archival_memory: list, recall_memory: RecallMemory):
        self.core_memory = core_memory
        self.archival_memory = archival_memory 
        self.recall_memory = recall_memory 

    def save(self, file_path: str) -> None:
        """Saves the current memory state to a file."""
        
        # Debug log for saving data
        logger.debug(f"Preparing to save data to {file_path}")

        # Use ipdb to set a breakpoint
        #ipdb.set_trace()  # Debug: Check memory state before saving
        archival_data = [{"memory": memory, "embedding": embedding.tolist()} for memory, embedding in self.archival_memory]

        data = {
            "core_memory": self.core_memory.to_dict(),
            "archival_memory": archival_data,
            "recall_memory": [message.to_dict() for message in self.recall_memory.messages],
        }

        logger.debug(f"Saving data to {file_path}: {json.dumps(data, indent=4)}")
        try:
            with open(file_path, "w") as f:
                json.dump(data, f)
            logger.info(f"Successfully saved memory data to {file_path}")
        except IOError as e:
            logger.error(f"IOError saving memory data: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving memory data: {e}")

    def load(self, file_path: str) -> None:
        """Loads a memory state from a file."""

        # Debug log for loading data
        logger.debug(f"Attempting to load data from {file_path}")

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            logger.debug(f"Data loaded from {file_path}: {json.dumps(data, indent=4)}")

            self.core_memory = BaseMemory.from_dict(data.get("core_memory", {}))

            self.archival_memory.clear()
            for entry in data.get("archival_memory", []):
                memory = entry["memory"]
                embedding = np.array(entry["embedding"], dtype=np.float32)
                self.archival_memory.append((memory, embedding))

            self.recall_memory.messages = [
                Message.from_dict(message_data) for message_data in data.get("recall_memory", [])
            ]

            logger.info(f"Successfully loaded memory data from {file_path}")

        except FileNotFoundError:
            logger.warning(f"Memory file not found at {file_path}. Initializing empty memory.")
            self.core_memory = BaseMemory()
            self.archival_memory = []
            self.recall_memory = RecallMemory()
        except json.JSONDecodeError:
            logger.error(f"JSON decoding failed for {file_path}. Initializing empty memory.")
            self.core_memory = BaseMemory()
            self.archival_memory = []
            self.recall_memory = RecallMemory()
        except Exception as e:
            logger.error(f"Unexpected error loading memory data from {file_path}: {e}")
            self.core_memory = BaseMemory()
            self.archival_memory = []
            self.recall_memory = RecallMemory()
