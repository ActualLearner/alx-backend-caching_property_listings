from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Retrieves the queryset of all properties, utilizing the cache.
    This function first checks if the 'all_properties' key exists in the cache.
    If it does (a cache hit), it returns the cached queryset.
    If it doesn't (a cache miss), it fetches all properties from the database,
    stores the queryset in the cache for 1 hour (3600 seconds), and then
    returns the queryset.
    """
    # Define the cache key
    cache_key = "all_properties"

    # Try to get the data from the cache
    queryset = cache.get(cache_key)

    # If the data is not in the cache (cache miss)
    if queryset is None:
        # Fetch the data from the database
        queryset = Property.objects.all()
        # Store the data in the cache for 1 hour (3600 seconds)
        cache.set(cache_key, queryset, 3600)

    # Return the queryset (either from cache or the fresh one from DB)
    return queryset
