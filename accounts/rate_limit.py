from django.core.cache import cache

import time

class TTLRateLimit:
    def __init__(self, prefix, limit, window):
        self.prefix = prefix
        self.limit = limit
        self.window = window

    def _make_key(self, client_id):
        return f'{self.prefix}:{client_id}'

    def allow(self, client_id):
        key = self._make_key(client_id)

        if cache.add(key, 1, timeout=self.window):
            return True

        count = cache.incr(key)

        return count <= self.limit

class BucketRateLimit:
    def __init__(self, prefix, limit, window):
        self.prefix = prefix
        self.limit = limit
        self.window = window

    def _get_bucket(self):
        now = time.time()
        bucket = now // self.window
        return now, bucket

    def _make_key(self, client_id, bucket):
        return f'{self.prefix}:{client_id}:{bucket}'

    def allow(self, client_id):
        now, bucket = self._get_bucket()
        bucket_end = (bucket + 1) * self.window
        ttl = bucket_end - now

        key = self._make_key(client_id, bucket)

        if cache.add(key, 1, timeout=ttl):
            return True

        count = cache.incr(key)
        return count <= self.limit
