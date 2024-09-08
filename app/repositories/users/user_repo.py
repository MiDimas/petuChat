from ..repo.base import BaseRepo
from .user_model import User


class UserRepo(BaseRepo):
    model = User
