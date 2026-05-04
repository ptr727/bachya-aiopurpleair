"""Define package exceptions."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientResponse
from aiohttp.client_exceptions import ClientError


class PurpleAirError(Exception):
    """Define a base exception."""

    pass


class NotFoundError(PurpleAirError):
    """Define an unknown resource."""

    pass


class InvalidRequestError(PurpleAirError):
    """Define an invalid request."""

    pass


class RequestError(PurpleAirError):
    """Define a general HTTP request error."""

    pass


class InvalidApiKeyError(RequestError):
    """Define a base exception."""

    pass


class ApiKeyTypeMismatchError(InvalidApiKeyError):
    """Define a WRITE-key-where-READ-required error (HTTP 403)."""

    pass


class ApiKeyRestrictedError(InvalidApiKeyError):
    """Define an API key restricted to a specific host/referrer (HTTP 403)."""

    pass


class ApiDisabledError(InvalidApiKeyError):
    """Define an endpoint disabled for this API key (HTTP 403)."""

    pass


class ProjectArchivedError(InvalidApiKeyError):
    """Define a project-archived error (HTTP 403)."""

    pass


class InvalidTokenError(InvalidApiKeyError):
    """Define an invalid-token error (HTTP 403)."""

    pass


class InvalidDataReadKeyError(InvalidRequestError):
    """Define a wrong per-sensor read key error (HTTP 400)."""

    pass


class InvalidFieldValueError(InvalidRequestError):
    """Define an unknown-field-requested error (HTTP 400)."""

    pass


class InvalidParameterValueError(InvalidRequestError):
    """Define a generic parameter validation failure (HTTP 400)."""

    pass


class MissingRequiredParameterError(InvalidRequestError):
    """Define a missing-required-parameter error (HTTP 400)."""

    pass


class InvalidRequestUrlError(InvalidRequestError):
    """Define an invalid-request-URL error (HTTP 400)."""

    pass


class InvalidTimestampError(InvalidRequestError):
    """Define an invalid-timestamp error (HTTP 400)."""

    pass


class InvalidTimestampSpanError(InvalidRequestError):
    """Define an invalid-timestamp-span error (HTTP 400)."""

    pass


class InvalidAverageError(InvalidRequestError):
    """Define an invalid-average error (HTTP 400)."""

    pass


class MissingFieldsParameterError(InvalidRequestError):
    """Define a missing-fields-parameter error (HTTP 400)."""

    pass


class InvalidShowValueError(InvalidRequestError):
    """Define an invalid-show-value error (HTTP 400)."""

    pass


class InvalidLocationTypeError(InvalidRequestError):
    """Define an invalid-location-type error (HTTP 400)."""

    pass


class InvalidModifiedSinceError(InvalidRequestError):
    """Define an invalid-modified-since error (HTTP 400)."""

    pass


class InvalidMaxAgeError(InvalidRequestError):
    """Define an invalid-max-age error (HTTP 400)."""

    pass


class InvalidCfError(InvalidRequestError):
    """Define an invalid-cf error (HTTP 400)."""

    pass


class InvalidBoundingBoxError(InvalidRequestError):
    """Define an invalid-bounding-box error (HTTP 400)."""

    pass


class MissingJsonPayloadError(InvalidRequestError):
    """Define a missing-JSON-payload error (HTTP 415)."""

    pass


class InvalidJsonPayloadError(InvalidRequestError):
    """Define an invalid-JSON-payload error (HTTP 400)."""

    pass


class RequiresHttpsError(PurpleAirError):
    """Define a requires-HTTPS error (HTTP 403)."""

    pass


class PaymentRequiredError(PurpleAirError):
    """Define an out-of-API-points error (HTTP 402)."""

    pass


class RateLimitExceededError(PurpleAirError):
    """Define a rate-limit-exceeded error (HTTP 429)."""

    pass


class DataInitializingError(PurpleAirError):
    """Define a data-initializing transient error (HTTP 503)."""

    pass


ERROR_CODE_MAP = {
    "ApiKeyMissingError": InvalidApiKeyError,
    "ApiKeyInvalidError": InvalidApiKeyError,
    "ApiKeyTypeMismatchError": ApiKeyTypeMismatchError,
    "ApiKeyRestrictedError": ApiKeyRestrictedError,
    "ApiDisabledError": ApiDisabledError,
    "ProjectArchivedError": ProjectArchivedError,
    "InvalidTokenError": InvalidTokenError,
    "InvalidDataReadKeyError": InvalidDataReadKeyError,
    "InvalidFieldValueError": InvalidFieldValueError,
    "InvalidParameterValueError": InvalidParameterValueError,
    "MissingRequiredParameterError": MissingRequiredParameterError,
    "InvalidRequestUrlError": InvalidRequestUrlError,
    "InvalidTimestampError": InvalidTimestampError,
    "InvalidTimestampSpanError": InvalidTimestampSpanError,
    "InvalidAverageError": InvalidAverageError,
    "MissingFieldsParameterError": MissingFieldsParameterError,
    "InvalidShowValueError": InvalidShowValueError,
    "InvalidLocationTypeError": InvalidLocationTypeError,
    "InvalidModifiedSinceError": InvalidModifiedSinceError,
    "InvalidMaxAgeError": InvalidMaxAgeError,
    "InvalidCfError": InvalidCfError,
    "InvalidBoundingBoxError": InvalidBoundingBoxError,
    "MissingJsonPayloadError": MissingJsonPayloadError,
    "InvalidJsonPayloadError": InvalidJsonPayloadError,
    "RequiresHttpsError": RequiresHttpsError,
    "PaymentRequiredError": PaymentRequiredError,
    "RateLimitExceededError": RateLimitExceededError,
    "DataInitializingError": DataInitializingError,
    "NotFoundError": NotFoundError,
}


def raise_error(
    resp: ClientResponse, payload: dict[str, Any], raising_err: ClientError | None
) -> None:
    """Raise the appropriate error based on the response data.

    Args:
        resp: An aiohttp ClientResponse.
        payload: An API response payload.
        raising_err: The aiohttp ClientError that caused the overall issue.

    Raises:
        exc: Raised upon an HTTP error.
    """
    if (error_code := payload.get("error")) is None:
        return

    exc_cls = ERROR_CODE_MAP.get(error_code, RequestError)
    raise exc_cls(
        f"Error while querying {resp.url}: {payload['description']}"
    ) from raising_err
