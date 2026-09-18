from django.core.cache import cache

DEFAULT_CACHE_TIMEOUT = 300

def get_cached_items(cache_key):
    return cache.get(cache_key)


def set_cached_items(cache_key, items):
    cache.set(
        cache_key,
        items,
        DEFAULT_CACHE_TIMEOUT
    )


# def invalidate_cache(*cache_keys):
#     cache.delete_many(cache_keys)

def invalidate_catalog_cache():
    cache.clear()

