# cache.py

import redis

class CacheHandler:
    """A Redis-based caching handler for storing and retrieving data."""

    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set_cache(self, key, value, expiration=3600):
        """Set a value in the cache with an expiration time."""
        self.client.setex(key, expiration, value)

    def get_cache(self, key):
        """Get a cached value by key."""
        return self.client.get(key)

    def delete_cache(self, key):
        """Delete a cached entry by key."""
        self.client.delete(key)
