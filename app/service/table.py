from app.repository.table import TableRepository
from app.schemas.table import TableIn

from typing import Annotated
from fastapi import Depends



class TableService:
    def __init__(self, repository: Annotated[TableRepository, Depends()]):
        self.repository = repository

    async def add_table(self, data: TableIn):
        data = data.model_dump()
        return await self.repository.add_one(data)
