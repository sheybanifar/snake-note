from django.test import TestCase
from django.core.cache import cache

from accounts.rate_limit import TTLRateLimit

class TTLRateLimitTests(TestCase):
    def setUp(self):
        self.limiter = TTLRateLimit('rate-limit', 3, 10)
        self.client_id = 'client-1'

    def test_allow_first_request(self):
        self.assertTrue(self.limiter.allow(self.client_id))

    def test_deny_after_limit_count(self):
        self.assertTrue(self.limiter.allow(self.client_id))
        self.assertTrue(self.limiter.allow(self.client_id))
        self.assertTrue(self.limiter.allow(self.client_id))
        self.assertFalse(self.limiter.allow(self.client_id))

        key = self.limiter._make_key(self.client_id)

        self.assertEqual(cache.get(key), 4)

    def tearDown(self):
        cache.clear()