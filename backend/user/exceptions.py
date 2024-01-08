from core.exceptions import BusinessException
from fastapi import status


class UserExists(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Пользователь существует"
    code = "user_exists"


class UserNotExists(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    detail_template = "Пользователь не сущетсвует"
    code = "user_not_exists"
