"""Retry logic with exponential backoff for API calls.

This module implements resilient retry patterns following best practices from
"AI Engineering" by Chip Huyen (Chapter 5: Building Resilient Systems).

Key principles:
- Exponential backoff to avoid overwhelming failing services
- Jitter to prevent thundering herd problem
- Detailed logging for debugging
- Configurable retry limits
"""

import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

from openai import APIError as OpenAIAPIError
from openai import RateLimitError

try:
    from .exceptions import APIError
except ImportError:
    from exceptions import APIError

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
) -> T:
    """Retries a function with exponential backoff and jitter.

    This implements the retry pattern recommended for LLM API calls:
    1. First attempt fails → wait base_delay seconds
    2. Second attempt fails → wait base_delay * exponential_base seconds
    3. Third attempt fails → wait base_delay * exponential_base^2 seconds
    ... up to max_delay

    Jitter adds randomness to prevent synchronized retries from multiple clients.

    Args:
        func: The function to retry. Should be a callable that may raise exceptions.
        max_attempts: Maximum number of attempts (default 3).
        base_delay: Initial delay in seconds (default 1.0).
        max_delay: Maximum delay in seconds (default 60.0).
        exponential_base: Base for exponential backoff (default 2.0).
        jitter: Whether to add random jitter to delays (default True).

    Returns:
        The return value of func if successful.

    Raises:
        APIError: If all retry attempts fail, raises APIError wrapping the last exception.

    Examples:
        >>> def flaky_api_call():
        ...     # Simulates an API that fails twice then succeeds
        ...     if random.random() < 0.7:
        ...         raise RateLimitError("Rate limited")
        ...     return {"result": "success"}
        >>> result = retry_with_backoff(flaky_api_call, max_attempts=5)
        >>> result["result"]
        'success'
    """
    last_exception: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            logger.debug(f"Attempt {attempt}/{max_attempts} for {func.__name__}")
            result = func()
            if attempt > 1:
                logger.info(
                    f"{func.__name__} succeeded on attempt {attempt}/{max_attempts}"
                )
            return result

        except (OpenAIAPIError, RateLimitError) as e:
            last_exception = e
            logger.warning(
                f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}"
            )

            if attempt == max_attempts:
                logger.error(
                    f"All {max_attempts} attempts failed for {func.__name__}"
                )
                break

            # Calculate delay with exponential backoff
            delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)

            # Add jitter: random value between 0 and delay
            if jitter:
                delay = random.uniform(0, delay)

            logger.info(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)

        except Exception as e:
            # For non-API errors, fail immediately without retry
            logger.error(f"Non-retryable error in {func.__name__}: {e}")
            raise APIError(f"Unexpected error: {str(e)}") from e

    # If we get here, all attempts failed
    if isinstance(last_exception, RateLimitError):
        raise APIError(
            "Rate limit exceeded after all retry attempts",
            status_code=429,
        ) from last_exception
    elif isinstance(last_exception, OpenAIAPIError):
        raise APIError(
            f"API error after all retry attempts: {str(last_exception)}",
            status_code=getattr(last_exception, "status_code", None),
        ) from last_exception
    else:
        raise APIError(
            f"Unknown error after all retry attempts: {str(last_exception)}"
        ) from last_exception
