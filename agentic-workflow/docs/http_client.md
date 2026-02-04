# AsyncHTTPClient

A robust async HTTP client built on top of `httpx` with automatic retry logic, exponential backoff, and comprehensive error handling.

## Features

- ✅ **Automatic Retry**: Retries failed requests with exponential backoff for transient errors (5xx, connection errors, timeouts)
- ✅ **Configurable Timeout**: Set custom timeout values for all requests
- ✅ **JSON Auto-parsing**: Automatically parse JSON responses
- ✅ **Custom Headers**: Support for default headers and per-request headers
- ✅ **Context Manager**: Proper resource management with async context manager protocol
- ✅ **Type Hints**: Full type annotations for better IDE support and type checking
- ✅ **Custom Exceptions**: Specific exception types for different error scenarios
- ✅ **HTTP Methods**: Support for GET, POST, PUT, and DELETE methods

## Installation

The `httpx` dependency is already included in the project.

## Usage

### Basic Example

```python
import asyncio
from agentic_workflow.http_client import AsyncHTTPClient

async def main():
    async with AsyncHTTPClient(base_url="https://api.example.com") as client:
        # GET request
        user = await client.get("/users/1")
        print(f"User: {user}")
        
        # POST request
        new_user = await client.post(
            "/users",
            json={"name": "John", "email": "john@example.com"}
        )
        print(f"Created: {new_user}")

asyncio.run(main())
```

See `examples/http_client_example.py` for more examples.

## Configuration Options

- `base_url`: Base URL for all requests
- `timeout`: Request timeout in seconds (default: 30.0)
- `default_headers`: Default headers for all requests
- `max_retries`: Maximum retry attempts (default: 3)
- `retry_backoff_factor`: Exponential backoff factor (default: 1.0)

## Exception Hierarchy

```
HTTPClientError (base exception)
├── HTTPTimeoutError
├── HTTPConnectionError
├── HTTPClientStatusError (4xx errors)
└── HTTPServerError (5xx errors)
```
