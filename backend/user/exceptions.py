from core.exceptions import BusinessException
from fastapi import status


class UserExists(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Пользователь {username} существует"
    code = "user_exists"
