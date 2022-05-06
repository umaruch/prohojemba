from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from server.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DB_URI.format("asyncpg"), echo=settings.DEBUG)
Base = declarative_base()

Session = sessionmaker(bind=engine, class_=AsyncSession)
