from pydantic import BaseModel


class TokensPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"