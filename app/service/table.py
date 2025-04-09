from typing import Annotated

from fastapi import Depends

from app.repository.table import TableRepository
from app.schemas.table import TableIn


class TableService:
    def __init__(self, repository: Annotated[TableRepository, Depends()]):
        self.repository = repository

    async def add_table(self, data: TableIn):
        data = data.model_dump()
        return await self.repository.add_one(data)

    async def get_tables(self):
        return await self.repository.get_all()

    async def delete_table(self, table_id: int):
        return await self.repository.delete_one(table_id)
