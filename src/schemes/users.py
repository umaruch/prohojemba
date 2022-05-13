from datetime import date, datetime


from src.schemes.base import ORMModel
from src.schemes.profiles import Profile, ProfilePreview


class BaseUser(ORMModel):
    id: int

class UserProfile(BaseUser):
    joined_at: date
    last_auth_at: datetime

    profile: Profile


class CurrentUserProfile(UserProfile):
    email: str


class UserProfilePreview(UserProfile):
    profile: ProfilePreview


