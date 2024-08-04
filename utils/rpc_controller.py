# rpm_controller.py

import time

class RPMController:
    """Controls the rate of requests per minute to avoid exceeding limits."""

    def __init__(self, max_requests_per_minute):
        self.max_requests_per_minute = max_requests_per_minute
        self.requests = []

    def allow_request(self):
        """Determine if a request can be allowed based on the rate limit."""
        current_time = time.time()
        self.requests = [t for t in self.requests if current_time - t < 60]

        if len(self.requests) < self.max_requests_per_minute:
            self.requests.append(current_time)
            return True
        return False
