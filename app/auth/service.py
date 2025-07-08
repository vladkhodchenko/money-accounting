from auth.models import User
from services.base import BaseService


class UserService(BaseService):
    model = User