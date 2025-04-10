import pytest
from fastapi import status
from sqlalchemy import select, text

from app.models.table import Table


@pytest.mark.anyio
async def test_create_table(client, db_session):
    data = {"name": "Luxury", "location": "first floor", "seats": 4}
    response = await client.post(url="/tables", json=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_get_all_tables(client, db_session):
    response = await client.get(url="/tables")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_delete_table(client, db_session, get_table_id):
    response = await client.delete(url=f"/tables/{get_table_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
