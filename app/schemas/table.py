from pydantic import BaseModel, ConfigDict


class TableBase(BaseModel):
    name: str
    location: str
    seats: int


class TableIn(TableBase):
    pass


class Table(TableBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
