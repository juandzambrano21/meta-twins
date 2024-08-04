# messages.py

import datetime
from typing import List, Dict, Optional

class Message:
    """Represents a single message in the conversation."""

    def __init__(self, role: str, content: str, created_at: Optional[datetime.datetime] = None):
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.datetime.now()


    def to_dict(self) -> Dict:
        """Converts the message to a dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Message":
        """Creates a Message object from a dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
        )


class RecallMemory:
    """Stores the history of messages in the conversation."""

    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message) -> None:
        """Adds a message to the recall memory."""
        self.messages.append(message)

    def search_by_text(self, query: str) -> List[Message]:
        """Searches for messages containing the query text."""
        return [message for message in self.messages if query.lower() in message.content.lower()]

    def search_by_date(self, start_date: datetime.datetime, end_date: datetime.datetime) -> List[Message]:
        """Searches for messages within a date range."""
        return [message for message in self.messages if start_date <= message.created_at <= end_date]

    def __len__(self):
        return len(self.messages)

    def __str__(self):
        return "\n".join([f"{message.created_at} - {message.role}: {message.content}" for message in self.messages])

    def clear(self):
        self.messages.clear()
