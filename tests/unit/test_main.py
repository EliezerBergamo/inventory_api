from fastapi.testclient import TestClient
from main import app

client = TestClient(app) # Create the test client

# Testing for errors logged in main.py

"""
4xx Errors (Client side)
"""

def test_bad_request_error():
    """
   Test the 400 Bad Request error handler.

   - **Steps**:
       1. Sends a GET request to a non-existent endpoint.
       2. Verifies if the response status code is 400.
       3. Verifies if the response JSON matches the expected error format.
       """
    response = client.get("/api/v1/non-existent-endpoint")
    assert response.status_code == 400
    assert response.json() == {"error": "Bad Request","message": "400: Bad Request", "status_code": 400}

def test_unauthorized_error():
    """
    Test the 401 Unauthorized error handler.

    - **Steps**:
        1. Sends a GET request to a protected resource without authentication.
        2. Verifies if the response status code is 401.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/protected-resource")
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized","message": "401: Unauthorized", "status_code": 401}

def test_forbidden_error():
    """
    Test the 403 Forbidden error handler.

    - **Steps**:
        1. Sends a GET request to a restricted resource without proper permissions.
        2. Verifies if the response status code is 403.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/restricted-resource")
    assert response.status_code == 403
    assert response.json() == {"error": "Forbidden","message": "403: Forbidden Handler", "status_code": 403}

def test_not_found_error():
    """
    Test the 404 Not Found error handler.

    - **Steps**:
        1. Sends a GET request to a non-existent resource.
        2. Verifies if the response status code is 404.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/non-existent-resource")
    assert response.status_code == 404
    assert response.json() == {"error": "Not Found","message": "404: Not Found", "status_code": 404}

def test_method_not_allowed_error():
    """
    Test the 405 Method Not Allowed error handler.

    - **Steps**:
        1. Sends a PUT request to an endpoint that only accepts GET.
        2. Verifies if the response status code is 405.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.put("/api/v1/method-not-allowed")
    assert response.status_code == 405
    assert response.json() == {"error": "Method Not Allowed","message": "405: Method Not Allowed", "status_code": 405}

def test_request_timeout_error():
    """
    Test the 408 Request Timeout error handler.

    - **Steps**:
        1. Sends a GET request to a slow endpoint.
        2. Verifies if the response status code is 408.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/slow-endpoint")
    assert response.status_code == 408
    assert response.json() == {"error": "Request Timeout","message": "408: Request Timeout", "status_code": 408}

def test_conflict_error():
    """
    Test the 409 Conflict error handler.

    - **Steps**:
        1. Sends a GET request to a resource that causes a conflict.
        2. Verifies if the response status code is 409.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/some-resource")
    assert response.status_code == 409
    assert response.json() == {"error": "Conflict","message": "409: Conflict", "status_code": 409}

def test_too_many_requests_error():
    """
    Test the 429 Too Many Requests error handler.

    - **Steps**:
        1. Sends a GET request to a rate-limited endpoint.
        2. Verifies if the response status code is 429.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/rate-limited-endpoint")
    assert response.status_code == 429
    assert response.json() == {"error": "Too Many Requests","message": "429: Too Many Requests", "status_code": 429}

"""
5xx Errors (Server side)
"""

def test_internal_server_error():
    """
    Test the 500 Internal Server Error handler.

    - **Steps**:
        1. Sends a GET request to an endpoint that triggers an internal server error.
        2. Verifies if the response status code is 500.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/trigger-error")
    assert response.status_code == 500
    assert response.json() == {"error": "Internal Server Error","message": "Internal Server Error", "status_code": 500}

def test_bad_gateway_requests_error():
    """
    Test the 502 Bad Gateway error handler.

    - **Steps**:
        1. Sends a GET request to a gateway endpoint.
        2. Verifies if the response status code is 502.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/gateway-endpoint")
    assert response.status_code == 502
    assert response.json() == {"error": "Bad Gateway","message": "502: Bad Gateway", "status_code": 502}

def test_service_unavailable_error():
    """
    Test the 503 Service Unavailable error handler.

    - **Steps**:
        1. Sends a GET request to a service unavailable endpoint.
        2. Verifies if the response status code is 503.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/service-unavailable-endpoint")
    assert response.status_code == 503
    assert response.json() == {"error": "Service Unavailable","message": "503: Service Unavailable", "status_code": 503}

def test_gateway_timeout_error():
    """
   Test the 504 Gateway Timeout error handler.

   - **Steps**:
       1. Sends a GET request to a gateway timeout endpoint.
       2. Verifies if the response status code is 504.
       3. Verifies if the response JSON matches the expected error format.
   """
    response = client.get("/api/v1/gateway-timeout-endpoint")
    assert response.json() == {"error": "Gateway Timeout","message": "504: Gateway Timeout", "status_code": 504}
    assert response.status_code == 504

def test_generic_exception_handler():
    """
    Test the generic exception handler for unexpected errors.

    - **Steps**:
        1. Sends a GET request to an endpoint that triggers an unexpected error.
        2. Verifies if the response status code is 500.
        3. Verifies if the response JSON matches the expected error format.
    """
    response = client.get("/api/v1/some-error-endpoint")
    assert response.status_code == 500
    assert response.json() == {"error": "Unexpected server error","message": "Unexpected server error", "status_code": 500}

def test_read_root():
    """
    Test the root endpoint.

    - **Steps**:
        1. Sends a GET request to the root endpoint ("/").
        2. Verifies if the response status code is 200.
        3. Verifies if the response JSON matches the expected message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
