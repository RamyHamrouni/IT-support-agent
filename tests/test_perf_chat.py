import pytest
import time

@pytest.mark.asyncio
async def test_chat_performance(async_client):
    payload = {
        "user_id": "user-123",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Hi, I'm having a problem with my office printer. "
                    "It keeps showing a paper jam error even though there is no paper stuck. "
                    "I've tried restarting it and checking the tray, but it still won't print. "
                    "Can you guide me through troubleshooting this issue?"
                )
            }
        ]
    }

    # Ensure app state categories exist
    from main import app
    app.state.all_categories = ["Hardware", "Network", "Software"]

    # Measure single request time
    start = time.perf_counter()
    response = await async_client.post("/chat", json=payload)
    duration = time.perf_counter() - start

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-123"
    assert isinstance(data["messages"], list)

    # Ensure the request completes in under 10 seconds
    assert duration < 10, f"Chat endpoint took too long: {duration:.3f} seconds"

    print(f"Single request duration: {duration:.3f} seconds")
