import pytest
from fastapi import status
from sqlalchemy import select

from app.models.reservation import Reservation


@pytest.mark.anyio
async def test_create_reservation(client, db_session, get_table_id):
    data = {
        "customer_name": "string",
        "table_id": get_table_id,
        "duration_minutes": 20,
        "reservation_time": "2025-04-10T19:49:25.924Z",
    }

    response = await client.post(url="/reservations", json=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_get_all_reservations(client, db_session):
    response = await client.get(url="/reservations")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_delete_reservation(client, db_session):
    res = await db_session.execute(select(Reservation))
    reservation_id = res.scalars().first().id
    response = await client.delete(url=f"/reservations/{reservation_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
