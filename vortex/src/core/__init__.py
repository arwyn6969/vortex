"""
Core module for Vortex of Enlightenment game.
""" 

from .redis_service import RedisService

# Create singleton instance of Redis service
redis_service = RedisService()

__all__ = ["redis_service"] 