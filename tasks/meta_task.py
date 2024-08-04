# tasks/meta_task.py

from typing import List, Dict, Any

class MetaTask:
    def __init__(
        self, 
        description: str, 
        tools: List[str], 
        dependencies: List[str] = [], 
        input_data: Dict[str, Any] = {}, 
        complexity: float = 1.0,
        context: str = "",
        status: str = ""  # Ensure status is handled
    ):
        self.description = description
        self.tools = tools
        self.dependencies = dependencies
        self.input_data = input_data
        self.result = None
        self.complexity = complexity  
        self.context = context  
        self.status = status  # Ensure status is handled

    def set_result(self, result):
        self.result = result
        self.status = 'completed'  # Mark task as completed

    def get_complexity(self) -> float:
        return self.complexity

    def is_completed(self) -> bool:
        """Check if the task is completed."""
        return self.status == 'completed'

    def set_context(self, context: str):
        """Set the context for the task execution."""
        self.context = context
