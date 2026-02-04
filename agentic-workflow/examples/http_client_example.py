"""
Example usage of AsyncHTTPClient.

This script demonstrates how to use the AsyncHTTPClient for making
HTTP requests with automatic retry, timeout, and error handling.
"""

import asyncio

from agentic_workflow.http_client import (
    AsyncHTTPClient,
    HTTPClientStatusError,
    HTTPConnectionError,
    HTTPTimeoutError,
)


async def example_basic_get() -> None:
    """Example: Basic GET request."""
    print("Example 1: Basic GET request")
    print("-" * 50)

    async with AsyncHTTPClient(base_url="https://jsonplaceholder.typicode.com") as client:
        try:
            # GET request - returns parsed JSON
            user = await client.get("/users/1")
            print(f"User: {user.get('name')} ({user.get('email')})")
        except Exception as e:
            print(f"Error: {e}")

    print()


async def example_post_request() -> None:
    """Example: POST request with JSON body."""
    print("Example 2: POST request with JSON body")
    print("-" * 50)

    async with AsyncHTTPClient(base_url="https://jsonplaceholder.typicode.com") as client:
        try:
            # POST request with JSON body
            new_post = await client.post(
                "/posts",
                json={
                    "title": "My New Post",
                    "body": "This is the content of my post",
                    "userId": 1,
                },
            )
            print(f"Created post with ID: {new_post.get('id')}")
            print(f"Title: {new_post.get('title')}")
        except Exception as e:
            print(f"Error: {e}")

    print()


async def example_with_headers() -> None:
    """Example: Request with custom headers."""
    print("Example 3: Request with custom headers")
    print("-" * 50)

    # Set default headers for all requests
    default_headers = {
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
    }

    async with AsyncHTTPClient(
        base_url="https://jsonplaceholder.typicode.com", default_headers=default_headers
    ) as client:
        try:
            # Request with additional headers
            posts = await client.get(
                "/posts",
                params={"userId": 1},
                headers={"X-Custom-Header": "CustomValue"},
            )
            print(f"Retrieved {len(posts)} posts")
        except Exception as e:
            print(f"Error: {e}")

    print()


async def example_error_handling() -> None:
    """Example: Error handling."""
    print("Example 4: Error handling")
    print("-" * 50)

    async with AsyncHTTPClient(
        base_url="https://jsonplaceholder.typicode.com", timeout=5.0
    ) as client:
        # Example 1: 404 Not Found (client error)
        try:
            await client.get("/nonexistent-endpoint")
        except HTTPClientStatusError as e:
            print(f"Client error caught: Status {e.status_code}")

        # Example 2: Timeout error
        try:
            async with AsyncHTTPClient(
                base_url="https://httpbin.org", timeout=0.001
            ) as timeout_client:
                await timeout_client.get("/delay/5")
        except HTTPTimeoutError as e:
            print(f"Timeout error caught: {e}")

        # Example 3: Connection error (invalid domain)
        try:
            async with AsyncHTTPClient(
                base_url="https://invalid-domain-that-does-not-exist-12345.com"
            ) as conn_client:
                await conn_client.get("/")
        except HTTPConnectionError as e:
            print(f"Connection error caught: {e}")

    print()


async def example_retry_behavior() -> None:
    """Example: Automatic retry behavior."""
    print("Example 5: Automatic retry with exponential backoff")
    print("-" * 50)

    # Configure retry settings
    async with AsyncHTTPClient(
        base_url="https://httpbin.org",
        max_retries=3,
        retry_backoff_factor=0.5,
        timeout=10.0,
    ) as client:
        try:
            # This endpoint randomly returns 500 errors
            # The client will automatically retry with exponential backoff
            result = await client.get("/status/200")
            print("Request successful!")
            print(f"Response: {result}")
        except Exception as e:
            print(f"Request failed after retries: {e}")

    print()


async def example_put_delete() -> None:
    """Example: PUT and DELETE requests."""
    print("Example 6: PUT and DELETE requests")
    print("-" * 50)

    async with AsyncHTTPClient(base_url="https://jsonplaceholder.typicode.com") as client:
        try:
            # PUT request to update a resource
            updated_post = await client.put(
                "/posts/1",
                json={
                    "id": 1,
                    "title": "Updated Title",
                    "body": "Updated body content",
                    "userId": 1,
                },
            )
            print(f"Updated post: {updated_post.get('title')}")

            # DELETE request
            await client.delete("/posts/1")
            print("Post deleted successfully")

        except Exception as e:
            print(f"Error: {e}")

    print()


async def main() -> None:
    """Run all examples."""
    print("=" * 50)
    print("AsyncHTTPClient Usage Examples")
    print("=" * 50)
    print()

    await example_basic_get()
    await example_post_request()
    await example_with_headers()
    await example_error_handling()
    await example_retry_behavior()
    await example_put_delete()

    print("=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
