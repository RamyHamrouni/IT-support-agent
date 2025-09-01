import pytest
import asyncio
import time

@pytest.mark.asyncio
async def test_chat_concurrent_requests(async_client):
    payload = {
        "user_id": "user-123",
        "messages": [
            {
                "role": "user",
                "content":"Hi, I'm having a problem with my office printer. "
            }
        ]
    }

    # Ensure app state categories exist
    from main import app
    app.state.all_categories = ["Hardware", "Network", "Software"]

    async def send_request():
        return await async_client.post("/chat", json=payload)

    num_requests = 5  # minimum concurrent requests
    start = time.perf_counter()
    responses = await asyncio.gather(*[send_request() for _ in range(num_requests)])
    duration = time.perf_counter() - start

    # Validate all responses
    for res in responses:
        assert res.status_code == 200
        data = res.json()
        assert data["user_id"] == "user-123"
        assert isinstance(data["messages"], list)

    # Optional: fail if concurrency is too slow (e.g., >15 seconds for 5 requests)
    assert duration < 15, f"Concurrent chat requests took too long: {duration:.3f} seconds"

    print(f"{num_requests} concurrent requests completed in {duration:.3f} seconds")
