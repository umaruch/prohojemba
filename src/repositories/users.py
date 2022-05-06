from sqlalchemy.future import select


from src.repositories.base import BaseRepository
from src.models.users import User


class UsersRepository(BaseRepository):
    async def test(self):
        query = select(User)
        result = await self.db_session.execute(query)
        print(result.scalars().all())