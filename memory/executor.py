# executor.py

from typing import Dict, List, Any
import numpy as np
from .embeddings import EmbeddingModel

class FunctionExecutor:
    def __init__(self, core_memory, archival_memory, recall_memory):
        from memory.base_memory import BaseMemory
        self.core_memory: BaseMemory = core_memory
        self.archival_memory = archival_memory
        self.recall_memory = recall_memory
        self.embedding_model = EmbeddingModel()

    def execute_function(self, function_call: Dict) -> str:
        """Executes a function call."""
        function_name = function_call["name"]
        args = function_call.get("args", {})

        if function_name == "add_memory":
            memory_content = args.get("content", "")
            embedding = self.embedding_model.embed(memory_content)
            print(f"Adding memory: {memory_content}, Embedding: {embedding}")  # Debugging
            self.archival_memory.append((memory_content, embedding))
            print(f"Archival Memory: {self.archival_memory}")  # Debugging
            return "Memory added successfully."

        elif function_name == "search_memory":
            query = args.get("query", "")
            top_k = args.get("top_k", 5)
            return self.search_archival_memory(query, top_k)

        elif function_name == "append_to_module":
            module_name = args.get("module_name", "")
            new_content = args.get("content", "")
            try:
                self.core_memory.get_module(module_name).append(new_content)
                return f"Content appended to module '{module_name}'."
            except ValueError as e:
                return str(e)

        elif function_name == "replace_in_module":
            module_name = args.get("module_name", "")
            old_content = args.get("old_content", "")
            new_content = args.get("new_content", "")
            try:
                self.core_memory.get_module(module_name).replace(old_content, new_content)
                return f"Content in module '{module_name}' replaced successfully."
            except ValueError as e:
                return str(e)

        elif function_name == "retrieve_messages":
            query = args.get("query", "")
            results = self.recall_memory.search_by_text(query)
            return f"Messages retrieved: {[str(msg) for msg in results]}"

        elif function_name == "clear_memory":
            memory_type = args.get("type", "all")
            return self.clear_memory(memory_type)

        return "Unknown function call."

    def search_archival_memory(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Searches for memories based on semantic similarity."""
        query_embedding = self.embedding_model.embed(query)
        similarities = [
            (self.embedding_model.similarity(query_embedding, memory_embedding), memory)
            for memory, memory_embedding in self.archival_memory
        ]
        top_matches = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]
        return [{"text": match[1], "score": match[0]} for match in top_matches]

    def clear_memory(self, memory_type: str) -> str:
        """Clears specified type of memory."""
        if memory_type == "core":
            self.core_memory.memory_modules.clear()
            return "Core memory cleared."
        elif memory_type == "archival":
            self.archival_memory.clear()
            return "Archival memory cleared."
        elif memory_type == "recall":
            self.recall_memory.clear()
            return "Recall memory cleared."
        else:
            self.core_memory.memory_modules.clear()
            self.archival_memory.clear()
            self.recall_memory.clear()
            return "All memory cleared."