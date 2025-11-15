"""
Simple in-memory cache for scraper results.

This helps avoid making too many requests to the same website.
Cache expires after a set time (default: 1 hour).
"""

from typing import Optional, Dict, Tuple
import time


class SimpleCache:
    """Simple in-memory cache with expiration."""
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache.
        
        Args:
            ttl_seconds: Time to live in seconds (default: 1 hour)
        """
        self.cache: Dict[str, Tuple[any, float]] = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[any]:
        """
        Get value from cache if it exists and hasn't expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self.cache:
            return None
        
        value, timestamp = self.cache[key]
        
        # Check if expired
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: any) -> None:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached values."""
        self.cache.clear()


# Global cache instance (1 hour TTL)
scraper_cache = SimpleCache(ttl_seconds=3600)

