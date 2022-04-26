from sqlalchemy.orm import sessionmaker


class DatabaseComponents:
    def __init__(self) -> None:
        self.session