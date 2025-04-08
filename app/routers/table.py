from fastapi import APIRouter, status, Depends
from typing import Annotated

from app.schemas.table import TableIn
from app.service.table import TableService

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_table(data: TableIn, service: Annotated[TableService, Depends()]):
    return await service.add_table(data)