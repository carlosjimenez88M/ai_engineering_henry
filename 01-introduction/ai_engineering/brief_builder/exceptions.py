"""Custom exceptions for brief builder.

This module defines a hierarchy of exceptions for better error handling
and clearer debugging. Following best practices from "AI Engineering" by
Chip Huyen, we use specific exceptions to differentiate between failure modes.
"""


class BriefBuilderError(Exception):
    """Base exception for all brief_builder errors.

    All custom exceptions in the brief_builder module inherit from this.
    This allows catching all brief_builder-specific errors with a single
    except clause if needed.

    Examples:
        >>> try:
        ...     raise BriefBuilderError("Something went wrong")
        ... except BriefBuilderError as e:
        ...     print(f"Brief builder error: {e}")
    """

    pass


class APIError(BriefBuilderError):
    """Exception raised for errors when calling external APIs.

    This includes OpenAI API errors such as:
    - Rate limiting (429)
    - Authentication failures (401)
    - Service unavailable (503)
    - Timeouts
    - Invalid requests (400)

    Attributes:
        message: Explanation of the error.
        status_code: HTTP status code if available.
        retry_after: Seconds to wait before retrying (from rate limit headers).

    Examples:
        >>> raise APIError("Rate limit exceeded", status_code=429, retry_after=60)
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        retry_after: int | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.retry_after = retry_after
        super().__init__(self.message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"(status: {self.status_code})")
        if self.retry_after:
            parts.append(f"(retry after: {self.retry_after}s)")
        return " ".join(parts)


class ValidationError(BriefBuilderError):
    """Exception raised for validation failures.

    This includes both input validation (temperature out of range,
    context too long) and output validation (malformed brief,
    missing required sections).

    Attributes:
        message: Explanation of the validation failure.
        field: The field that failed validation (optional).
        value: The invalid value (optional).

    Examples:
        >>> raise ValidationError(
        ...     "Temperature out of range",
        ...     field="temperature",
        ...     value=3.0
        ... )
    """

    def __init__(
        self, message: str, field: str | None = None, value: str | None = None
    ):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.field:
            parts.append(f"(field: {self.field})")
        if self.value:
            parts.append(f"(value: {self.value})")
        return " ".join(parts)


class ConfigurationError(BriefBuilderError):
    """Exception raised for configuration errors.

    This includes:
    - Missing required environment variables (OPENAI_API_KEY)
    - Invalid configuration values
    - Missing configuration files

    This error is typically not recoverable without user intervention.

    Examples:
        >>> raise ConfigurationError("OPENAI_API_KEY not set in environment")
    """

    pass
