from support_copilot.infrastructure.security.rate_limit import InMemoryRateLimiter


def test_rate_limiter_blocks_after_threshold():
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("ip1") is True
    assert limiter.allow("ip1") is True
    assert limiter.allow("ip1") is False
