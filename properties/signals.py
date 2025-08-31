from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging as logger

@receiver([post_save, post_delete], sender=Property)
def invalidate_property_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate the 'all_properties' cache key when a new Property is created or updated
    """
    cache.delete('all_properties')
    logger.error(f"cache invalidated for all_properties")