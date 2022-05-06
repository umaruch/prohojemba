import aioredis


from src.core.settings import RedisSettings


class RedisComponents:
    def __init__(self, settings: RedisSettings) -> None:
        self.pool = aioredis.BlockingConnectionPool.from_url(**settings.kwargs, max_connections=5)

    def __call__(self):
        return aioredis.Redis(connection_pool=self.pool)

    async def disconnect(self):
        await self.pool.disconnect()
                                                                      