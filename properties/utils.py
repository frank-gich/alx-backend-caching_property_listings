from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Fetch all properties from Redis cache if available,
    otherwise query the DB and cache the result for 1 hour.
    """
    properties = cache.get("all_properties")

    if properties is None:
        properties = Property.objects.all()
        cache.set("all_properties", properties, 3600)  # cache for 1 hour

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss statistics and compute hit ratio.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.info("Redis Cache Metrics: %s", metrics)
        return metrics

    except Exception as e:
        logger.error("Failed to fetch Redis metrics: %s", str(e))
        return {"error": str(e)}
