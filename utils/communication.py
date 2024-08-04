# communication.py

import threading

class EnhancedCommunication:
    """Handles inter-agent messaging using a thread-safe approach."""

    def __init__(self):
        self.messages = {}
        self.lock = threading.Lock()

    def send_message(self, agent_id, message):
        """Send a message to a specific agent."""
        with self.lock:
            if agent_id not in self.messages:
                self.messages[agent_id] = []
            self.messages[agent_id].append(message)

    def receive_message(self, agent_id):
        """Receive messages for a specific agent."""
        with self.lock:
            return self.messages.pop(agent_id, [])

    def clear_messages(self):
        """Clears all messages."""
        with self.lock:
            self.messages.clear()
