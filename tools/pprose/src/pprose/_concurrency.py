"""Bounded async concurrency helper.

Combines an asyncio.Semaphore (parallelism cap) with an aiolimiter leaky
bucket (per-second rate cap) so a batch of N coroutines doesn't exhaust a
downstream rate limit and doesn't fan out beyond what the host machine or
remote service can comfortably handle.

Public API: `gather_limited(*coros, max_concurrent, max_rps, return_exceptions)`.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import TypeVar

from aiolimiter import AsyncLimiter

T = TypeVar("T")


async def gather_limited(
    *coros: Awaitable[T],
    max_concurrent: int = 8,
    max_rps: float = 4.0,
    return_exceptions: bool = False,
) -> list:
    """Rate-limited variant of asyncio.gather().

    Each coroutine acquires a slot from a Semaphore and a token from a
    leaky-bucket limiter before running. Results are returned in input order.

    Args:
        *coros: Awaitables to schedule.
        max_concurrent: Maximum simultaneous in-flight coroutines.
        max_rps: Maximum coroutine starts per second across all workers.
        return_exceptions: If True, exceptions become entries in the result
            list rather than propagating. Useful for batch eval where one
            failed doc shouldn't abort the rest.
    """
    if not coros:
        return []

    semaphore = asyncio.Semaphore(max_concurrent)
    rate_limiter = AsyncLimiter(max_rps, 1.0)

    async def _wrapped(awaitable: Awaitable[T]) -> T:
        async with semaphore, rate_limiter:
            return await awaitable

    return await asyncio.gather(
        *(_wrapped(c) for c in coros),
        return_exceptions=return_exceptions,
    )
