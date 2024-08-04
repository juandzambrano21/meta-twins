from typing import Dict, Any

class MemoryModule:
    """Represents a single section of memory with a limit."""

    def __init__(self, name: str, limit: int, content: str = ""):
        self.name = name
        self.limit = limit
        self.content = content

    def append(self, new_content: str) -> None:
        """Appends content to the memory module."""
        
        # Check content length before appending
        if len(self.content) + len(new_content) > self.limit:
            raise ValueError(f"Appending exceeds the memory limit of {self.limit} characters.")
        self.content += new_content

    def replace(self, old_content: str, new_content: str) -> None:
        """Replaces existing content in the memory module."""
        
        # Ensure old content exists
        if old_content not in self.content:
            raise ValueError(f"Content to replace not found in memory module '{self.name}'.")
        
        # Replace and validate length
        self.content = self.content.replace(old_content, new_content)
        if len(self.content) > self.limit:
            raise ValueError(f"Replacement exceeds the memory limit of {self.limit} characters.")

    def to_dict(self) -> Dict[str, Any]:
        """Converts the memory module content to a dictionary."""
        return {
            "name": self.name,
            "limit": self.limit,
            "content": self.content
        }

class BaseMemory:
    """Base class for memory management."""

    def __init__(self):
        self.memory_modules: Dict[str, MemoryModule] = {}

    def add_module(self, name: str, limit: int, content: str = "") -> None:
        """Adds a new memory module."""
        
        # Check if module already exists
        if name in self.memory_modules:
            raise ValueError(f"Memory module '{name}' already exists.")
        
        # Add new module
        self.memory_modules[name] = MemoryModule(name, limit, content)

    def get_module(self, name: str) -> MemoryModule:
        """Retrieves a memory module by name."""
        
        # Ensure module exists
        if name not in self.memory_modules:
            raise ValueError(f"Memory module '{name}' not found.")
        
        # Return module
        return self.memory_modules[name]

    def to_dict(self) -> Dict[str, Any]:
        """Converts all memory modules to a dictionary."""
        
        # Convert memory modules to dict
        return {name: module.to_dict() for name, module in self.memory_modules.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseMemory":
        """Creates a BaseMemory instance from a dictionary."""
        
        # Create new memory instance
        memory = cls()
        for name, module_data in data.items():
            module = MemoryModule(name, module_data["limit"], module_data["content"])
            memory.memory_modules[name] = module
        
        # Return memory instance
        return memory
