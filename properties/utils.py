import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

# Get a logger instance for this module
logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Retrieves the queryset of all properties, utilizing the cache.
    (This function remains unchanged)
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

    This function gets a raw connection to the Redis client, fetches server
    statistics, calculates the cache hit ratio, and logs the metrics
    using logger.error as required.

    Returns:
        A dictionary containing the number of hits, misses, and the calculated
        hit ratio.
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total_requests = hits + misses

    # Calculate the hit ratio using the specified one-line conditional expression.
    hit_ratio = (hits / total_requests * 100) if total_requests > 0 else 0

    # Log metrics using logger.error as strictly required.
    logger.error("--- Redis Cache Metrics ---")
    logger.error(f"  Cache Hits:   {hits}")
    logger.error(f"  Cache Misses: {misses}")
    logger.error(f"  Total Lookups: {total_requests}")
    logger.error(f"  Hit Ratio:    {hit_ratio:.2f}%")
    logger.error("---------------------------")

    metrics_dict = {"hits": hits, "misses": misses, "hit_ratio": hit_ratio}

    return metrics_dict
