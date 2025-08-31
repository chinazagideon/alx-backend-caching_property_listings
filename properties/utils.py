from django.core.cache import cache
from .models import Property
import os

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