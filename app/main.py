from contextlib import asynccontextmanager

from fastapi import FastAPI

# from app.config.db import database, setup_db
from app.routers import reservation, table

# @asynccontextmanager
# async def db_lifespan(application: FastAPI):
#     # configure_logging()
#     await setup_db()
#     yield
#     await database.close_db()


app = FastAPI(title="Booking service API", root_path="/api")

app.include_router(table.router)
app.include_router(reservation.router)
