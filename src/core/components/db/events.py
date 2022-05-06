import logging
from fastapi import FastAPI


from src.core.settings import DatabaseSettings
from src.core.components.db.components import DatabaseComponents


async def connect_to_db(app: FastAPI, settings: DatabaseSettings) -> None:
    logging.debug("Connect to PostgreSQL Server...")
    app.state.db = DatabaseComponents(settings)
    logging.debug("Connected to PostgreSQL Server.")


async def close_all_db_connections(app: FastAPI) -> None:
    logging.debug("Clossing all PostgreSQL sessions...")
    await app.state.db.disconnect()
    logging.debug("All PostgreSQL sessions clossed.")