from apps.auth.models import User
from services.database.base import BaseService


class UserService(BaseService):
    model = User
