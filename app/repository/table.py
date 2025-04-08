from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import database
from app.models.table import Table
from app.repository.base import BaseRepository


class TableRepository(BaseRepository):
    def __init__(self, session: Annotated[AsyncSession, Depends(database.get_session)]):
        self.session = session
        super().__init__(session, Table)
