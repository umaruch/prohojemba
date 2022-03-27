from curses import echo
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from server.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DB_URI, echo=True)
Base = declarative_base(bind=engine)

Session = sessionmaker(bind=engine, class_=AsyncSession)
