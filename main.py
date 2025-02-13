from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.database.connection import engine, Base
from app.api.v1 import auth
from app.api.v1 import inventory
from app.utils.errors import router as errors_router
from app.utils.error_handlers import (
    bad_request_handler,
    unauthorized_handler,
    forbidden_handler,
    not_found_handler,
    method_not_allowed_handler,
    request_timeout_handler,
    conflict_handler,
    too_many_requests_handler,
    internal_server_error_handler,
    bad_gateway_handler,
    service_unavailable_handler,
    gateway_timeout_handler,
    unknown_error_handler
)

# Create the FastAPI application
app = FastAPI(
    title="Inventory Management APi",
    description="API for product inventory management",
    version="1.0.0",
)

# Exception handler to format errors in a custom way
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    """
    Custom exception handler for HTTP errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The HTTPException instance containing error details.

    - **Returns**:
        - A JSONResponse with the error details formatted in a custom way.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.detail,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

# Include error routers
app.include_router(errors_router, prefix="/api/v1")

# Include inventory routers
app.include_router(inventory.router, prefix="/api/v1")

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Include auth routers
app.include_router(auth.router, prefix="/api/v1")

# Example route for testing the API
@app.get("/")
def read_root():
    """
    Root endpoint for testing the API.

    - **Returns**:
        - A JSON response with a welcome message.
    """
    return {"message": "Hello World"}

# Register error handlers
app.add_exception_handler(400, bad_request_handler)
app.add_exception_handler(401, unauthorized_handler)
app.add_exception_handler(403, forbidden_handler)
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(405, method_not_allowed_handler)
app.add_exception_handler(408, request_timeout_handler)
app.add_exception_handler(409, conflict_handler)
app.add_exception_handler(429, too_many_requests_handler)
app.add_exception_handler(500, internal_server_error_handler)
app.add_exception_handler(502, bad_gateway_handler)
app.add_exception_handler(503, service_unavailable_handler)
app.add_exception_handler(504, gateway_timeout_handler)

# Generic handler for unknown errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Generic exception handler for unknown errors.

    - **Parameters**:
        - `request`: The incoming request.
        - `exc`: The exception instance.

    - **Returns**:
        - A JSONResponse with the error details formatted by the unknown_error_handler.
    """
    return await unknown_error_handler(request, exc)
