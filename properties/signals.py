from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

# The receiver decorator connects our function to Django's signals.
# We listen to two signals: post_save and post_delete.
# We only care about signals sent from the Property model (sender=Property).
@receiver([post_save, post_delete], sender=Property)
def invalidate_property_cache(sender, instance, **kwargs):
    """
    Invalidates the 'all_properties' cache key whenever a Property
    instance is saved (created/updated) or deleted.
    """
    cache_key = 'all_properties'
    # Simply delete the key from the cache.
    # The next time get_all_properties() is called, it will be a cache miss.
    cache.delete(cache_key)
    # The following print statement is helpful for debugging to see the signal in action.
    print(f"Cache invalidated for key '{cache_key}' due to change in {instance}.")```
