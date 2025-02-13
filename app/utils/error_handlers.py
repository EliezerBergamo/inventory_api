from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import Response

# Dictionary of error messages for each status code
ERROR_MESSAGES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    409: "Conflict",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

# Standard error response format
def error_response(status_code: int, message: str):
    """
    Generates a standardized error response in JSON format.

    - **Parameters**:
        - `status_code`: The HTTP status code for the error.
        - `message`: A descriptive message about the error.

    - **Returns**:
        - A JSONResponse containing the error details.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "error": ERROR_MESSAGES.get(status_code, "Unknown Error"),
            "message": message,
            "status_code": status_code
        }
    )

"""
4xx Errors (Client side)
"""

# Error 400 (Bad Request)
async def bad_request_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 400 Bad Request errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 400 errors.
    """
    return error_response(400, str(exc))

# Error 401 (Unauthorized)
async def unauthorized_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 401 Unauthorized errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 401 errors.
    """
    return error_response(401, str(exc))

# Error 403 (Forbidden)
async def forbidden_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 403 Forbidden errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 403 errors.
    """
    return error_response(403, str(exc))

# Error 404 (Not Found)
async def not_found_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 404 Not Found errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 404 errors.
    """
    return error_response(404, str(exc))

# Error 405 (Method Not Allowed)
async def method_not_allowed_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 405 Method Not Allowed errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 405 errors.
    """
    return error_response(405, str(exc))

# Error 408 (Request Timeout)
async def request_timeout_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 408 Request Timeout errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 408 errors.
    """
    return error_response(408, str(exc))

# Error 409 (Conflict)
async def conflict_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 409 Conflict errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 409 errors.
    """
    return error_response(409, str(exc))

# Error 429 (Too Many Requests)
async def too_many_requests_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 429 Too Many Requests errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 429 errors.
    """
    return error_response(429, str(exc))

"""
5xx Errors (Server side)
"""

# Error 500 (Internal Server Error)
async def internal_server_error_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 500 Internal Server Error errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 500 errors.
    """
    return error_response(500, "An unexpected error occurred.")

# Error 502 (Bad Gateway)
async def bad_gateway_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 502 Bad Gateway errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 502 errors.
    """
    return error_response(502, str(exc))

# Error 503 (Service Unavailable)
async def service_unavailable_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 503 Service Unavailable errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 503 errors.
    """
    return error_response(503, str(exc))

# Error 504 (Gateway Timeout)
async def gateway_timeout_handler(request: Request, exc: Exception) -> Response:
    """
    Handles 504 Gateway Timeout errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for 504 errors.
    """
    return error_response(504, str(exc))

# Generic handler for unknown errors
async def unknown_error_handler(request: Request, exc: Exception) -> Response:
    """
    Handles unknown or unhandled errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception that triggered the error.

    - **Returns**:
        - A standardized error response for unknown errors.
    """
    return error_response(500, "An unknown error occurred.")
