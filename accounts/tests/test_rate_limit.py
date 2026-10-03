from django.test import TestCase
from django.core.cache import cache

from unittest.mock import patch

from accounts.rate_limit import TTLRateLimit, BucketRateLimit

# This class is used to test behaviors of "TTL rate limiter"

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

# This class is used to test behaviors of "Bucket rate limiter"

class BucketRateLimitTests(TestCase):
    def setUp(self):
        self.limiter = BucketRateLimit('test', 3, 10)
        self.client_id = 'client-1'

    @patch('accounts.rate_limit.time.time')
    def test_bucket_calculation_correctness(self, mock_time):
        mock_time.return_value = 100
        now, bucket = self.limiter._get_bucket()

        self.assertEqual(now, 100),
        self.assertEqual(bucket, 10)

    @patch('accounts.rate_limit.time.time')
    def test_bucket_changes_at_boundary(self, mock_time):
        mock_time.return_value = 100
        bucket1 = self.limiter._get_bucket()[1]

        mock_time.return_value = 110
        bucket2 = self.limiter._get_bucket()[1]

        self.assertEqual(bucket1, 10)
        self.assertEqual(bucket2, 11)


    def test_requests_are_allowed_until_limit(self):
        self.assertTrue(self.limiter.allow(self.client_id))
        self.assertTrue(self.limiter.allow(self.client_id))
        self.assertTrue(self.limiter.allow(self.client_id))

        self.assertFalse(self.limiter.allow(self.client_id))

    @patch('accounts.rate_limit.time.time')
    def test_new_bucket_new_cache_key(self, mock_time):
        mock_time.return_value = 100

        _, bucket_before = self.limiter._get_bucket()
        key_before = self.limiter._make_key(self.client_id, bucket_before)

        mock_time.return_value = 110

        _, bucket_after = self.limiter._get_bucket()
        key_after = self.limiter._make_key(self.client_id, bucket_after)

        self.assertNotEqual(bucket_before, bucket_after)
        self.assertNotEqual(key_before, key_after)

    def tearDown(self):
        cache.clear()