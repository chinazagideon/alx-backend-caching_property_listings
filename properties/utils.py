from django.core.cache import cache
from .models import Property
import os
import logging
from django_redis import get_redis_connection
from django.core.cache import cache


def get_redis_cache_metrics():
    """
    Retrieves and logs cache hit/miss metrics from Redis 
    """

    #get redis lowlevel connection client
    client = get_redis_connection("default")

    #get server information
    info = client.info('keyspace')

    # keyspace_hits and keyspace_misses
    try:
        keyspace_hits = int(info['keyspace_hits'])
        keyspace_misses = int(info['keyspace_misses'])
        total_requests = keyspace_misses + keyspace_hits

        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        
    except (KeyError, ValueError):
        hit_ratio = 0
        total_requests = 0
        keyspace_hits = 0
        keyspace_misses = 0
    
    #log the metrics
    logging.error(f'Redis cache Metrics:')
    logging.error(f"  - Keyspace Hits: {keyspace_hits}")
    logging.error(f"  - Keyspace Misses: {keyspace_misses}")
    logging.error(f"  - Hit Ratio: {hit_ratio:.2f}%" if isinstance(hit_ratio, float) else f"  - Hit Ratio: {hit_ratio}")

    return {
        'keyspace_hits': keyspace_hits,
        'keyspace_misses': keyspace_misses,
        'hit_ratio': hit_ratio
    }

def get_all_properties():
    """
    Get all properties from the cache or database
    """
    properties = cache.get('all_properties')

    # Check if the cache is empty
    if properties is None:

        # Get all properties from the database
        properties = Property.objects.all()

        # Set the cache for 15 minutes
        cache.set('all_properties', properties, int(os.getenv('CACHE_DURATION', 3600))) # 1 hour
    else:
        # Get the cache
        properties = cache.get('all_properties')
    return properties