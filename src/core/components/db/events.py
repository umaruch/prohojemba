import logging
from fastapi import FastAPI


from src.core.settings import Settings
from src.core.components.db.components import DatabaseComponents


async def connect_to_db(app: FastAPI, settings: Settings) -> None:
    logging.debug("Connect to PostgreSQL Server...")
    app.state.db = DatabaseComponents(settings.database)
    logging.debug("Connected to PostgreSQL Server.")


async def close_all_db_connections(app: FastAPI) -> None:
    logging.debug("Clossing all PostgreSQL sessions...")
    await app.state.db.engine.dispose()
    logging.debug("All PostgreSQL sessions clossed.")