import pytest
from fastapi import status
from sqlalchemy import text


@pytest.mark.anyio
async def test_create_table(get_client, db_session):
    data = {"name": "Luxury", "location": "first floor", "seats": 4}
    response = await get_client.post(url="/tables", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content == {"name": "Luxury", "location": "first floor", "seats": 4}
