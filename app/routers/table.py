from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.table import TableIn, Table
from app.service.table import TableService

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=Table)
async def create_table(data: TableIn, service: Annotated[TableService, Depends()]):
    return await service.add_table(data)

@router.get(path="", status_code=status.HTTP_200_OK, response_model=list[Table])
async def get_tables(service: Annotated[TableService, Depends()]):
    return await service.get_tables()
