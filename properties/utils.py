from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property


def get_all_properties():
    """
    Retrieves the queryset of all properties, utilizing the cache.
    (This function remains unchanged from the previous step)
    """
    cache_key = "all_properties"
    queryset = cache.get(cache_key)
    if queryset is None:
        queryset = Property.objects.all()
        cache.set(cache_key, queryset, 3600)
    return queryset


def get_redis_cache_metrics():
    """
    Connects to Redis to retrieve and analyze cache hit/miss statistics.

    This function gets a raw connection to the Redis client, fetches the server
    statistics using the INFO command, and calculates the cache hit ratio.

    Returns:
        A dictionary containing the number of hits, misses, and the calculated
        hit ratio as a percentage.
    """
    # Use the django_redis utility to get the raw redis-py client
    redis_conn = get_redis_connection("default")

    # The .info() command returns a dictionary of all Redis server stats
    info = redis_conn.info()

    # Extract the relevant keyspace statistics, defaulting to 0 if not present
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total_requests = hits + misses

    # Calculate the hit ratio, handling the division-by-zero case
    if total_requests > 0:
        # We multiply by 100 to get a percentage
        hit_ratio = (hits / total_requests) * 100
    else:
        hit_ratio = 0.0

    # Log the metrics to the console for easy analysis during development
    print("--- Redis Cache Metrics ---")
    print(f"  Cache Hits:   {hits}")
    print(f"  Cache Misses: {misses}")
    print(f"  Total Lookups: {total_requests}")
    print(f"  Hit Ratio:    {hit_ratio:.2f}%")
    print("---------------------------")

    metrics_dict = {"hits": hits, "misses": misses, "hit_ratio": hit_ratio}

    return metrics_dict
