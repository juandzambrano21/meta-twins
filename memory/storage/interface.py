# memory/storage/interface.py

from typing import Any, Dict, List
from datetime import datetime
import json

class Storage:
        def __init__(self):
            self.storage = []  # List to store entries
            self.current_id = 0  # Incremental ID for each entry

        def save(self, value: Any, metadata: Dict[str, Any]) -> None:
            """Save a value with associated metadata."""
            entry = {
                "id": self.current_id,
                "value": value,
                "metadata": metadata,
                "created_at": datetime.now().isoformat()
            }
            self.storage.append(entry)
            self.current_id += 1
            print(f"Saved entry: {entry}")

        def search(self, query: str) -> List[Dict[str, Any]]:
            """Search for entries containing the query in either the value or metadata."""
            results = []
            for entry in self.storage:
                entry_data = json.dumps(entry)  # Convert entry to JSON string
                if query.lower() in entry_data.lower():  # Case-insensitive search
                    results.append(entry)
            return results

        def reset(self) -> None:
            """Reset the storage by clearing all entries."""
            self.storage = []
            self.current_id = 0
            print("Storage has been reset.")

        def append(self, module_name: str, new_content: str) -> None:
            """Append new content to the value of a specific module."""
            for entry in self.storage:
                if entry['metadata'].get('module_name') == module_name:
                    entry['value'] += new_content
                    print(f"Appended new content to module '{module_name}'.")
                    return
            raise ValueError(f"Module '{module_name}' not found.")

        def replace(self, module_name: str, old_content: str, new_content: str) -> None:
            """Replace old content with new content in a specific module."""
            for entry in self.storage:
                if entry['metadata'].get('module_name') == module_name:
                    if old_content in entry['value']:
                        entry['value'] = entry['value'].replace(old_content, new_content)
                        print(f"Replaced content in module '{module_name}'.")
                    else:
                        raise ValueError(f"Old content not found in module '{module_name}'.")
                    return
            raise ValueError(f"Module '{module_name}' not found.")

        def search_by_text(self, query: str) -> List[Any]:
            """Search entries where the text contains the query."""
            results = []
            for entry in self.storage:
                if query.lower() in entry['value'].lower():
                    results.append(entry)
            return results

        def search_by_date(self, start_date: str, end_date: str) -> List[Any]:
            """Search entries created within a specific date range."""
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            results = []
            for entry in self.storage:
                entry_date = datetime.fromisoformat(entry['created_at'])
                if start <= entry_date <= end:
                    results.append(entry)
            return results