from fastapi import APIRouter, HTTPException, status

# Create the APIRouter instance for error endpoints
router = APIRouter()

"""
4xx Errors (Client side)
"""

@router.get("/non-existent-endpoint")
async def bad_request_error():
    """
    Simulates a 400 Bad Request error.

    - **Raises**:
        - HTTPException (400): With the detail "Bad Request".
    """
    raise HTTPException(status_code=400, detail="Bad Request")

@router.get("/protected-resource")
async def unauthorized_error():
    """
    Simulates a 401 Unauthorized error.

    - **Raises**:
        - HTTPException (401): With the detail "Unauthorized".
    """
    raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/restricted-resource")
async def forbidden_error():
    """
    Simulates a 403 Forbidden error.

    - **Raises**:
        - HTTPException (403): With the detail "Forbidden Handler".
    """
    raise HTTPException(status_code=403, detail="Forbidden Handler")

@router.get("/non-existent-resource")
async def not_found_error():
    """
    Simulates a 404 Not Found error.

    - **Raises**:
        - HTTPException (404): With the detail "Not Found".
    """
    raise HTTPException(status_code=404, detail="Not Found")

@router.get("/method-not-allowed")
async def method_not_allowed_error():
    """
    Simulates a 405 Method Not Allowed error.

    - **Raises**:
        - HTTPException (405): With the detail "Method Not Allowed".
    """
    raise HTTPException(status_code=405, detail="Method Not Allowed")

@router.get("/slow-endpoint")
async def request_timeout_error():
    """
    Simulates a 408 Request Timeout error.

    - **Raises**:
        - HTTPException (408): With the detail "Request Timeout".
    """
    raise HTTPException(status_code=408, detail="Request Timeout")

@router.get("/some-resource")
async def conflict_error():
    """
    Simulates a 409 Conflict error.

    - **Raises**:
        - HTTPException (409): With the detail "Conflict".
    """
    raise HTTPException(status_code=409, detail="Conflict")

@router.get("/rate-limited-endpoint")
async def too_many_requests_error():
    """
    Simulates a 429 Too Many Requests error.

    - **Raises**:
        - HTTPException (429): With the detail "Too Many Requests".
    """
    raise HTTPException(status_code=429, detail="Too Many Requests")

"""
5xx Errors (Server side)
"""

@router.get("/trigger-error")
async def internal_server_error():
    """
    Simulates a 500 Internal Server Error.

    - **Raises**:
        - HTTPException (500): With the detail "Internal Server Error".
    """
    raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/gateway-endpoint")
async def bad_gateway_error():
    """
    Simulates a 502 Bad Gateway error.

    - **Raises**:
        - HTTPException (502): With the detail "Bad Gateway".
    """
    raise HTTPException(status_code=502, detail="Bad Gateway")

@router.get("/service-unavailable-endpoint")
async def service_unavailable_error():
    """
    Simulates a 503 Service Unavailable error.

    - **Raises**:
        - HTTPException (503): With the detail "Service Unavailable".
    """
    raise HTTPException(status_code=503, detail="Service Unavailable")

@router.get("/gateway-timeout-endpoint")
async def gateway_timeout_error():
    """
    Simulates a 504 Gateway Timeout error.

    - **Raises**:
        - HTTPException (504): With the detail "Gateway Timeout".
    """
    raise HTTPException(status_code=504, detail="Gateway Timeout")

@router.get("/some-error-endpoint")
async def generic_exception_handler():
    """
    Simulates a generic 500 Internal Server Error.

    - **Raises**:
        - HTTPException (500): With the detail "Unexpected server error".
    """
    raise HTTPException(
        status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected server error"
    )
