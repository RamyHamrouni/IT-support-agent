import pytest

@pytest.mark.asyncio
async def test_read_main(async_client) -> None:
    payload = {
        "user_id": "user-123",
        "messages": [
            {"role": "user", "content": "I have a problem with my printer"}
        ]
    }

    # Ensure app state categories exist
    from main import app
    app.state.all_categories = ["Hardware", "Network", "Software"]

    response = await async_client.post("/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["user_id"] == "user-123"
    assert "messages" in data
    assert isinstance(data["messages"], list)
