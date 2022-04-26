from sqlalchemy.orm import sessionmaker


from core.settings import DatabaseSettings


class DatabaseComponents:
    def __init__(self, settings: DatabaseSettings) -> None:
        
        self.session