from core.exceptions import BusinessException
from fastapi import status


class UserExists(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Пользователь существует"
    code = "user_exists"


class UserNotExists(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    detail_template = "Пользователь не существует"
    code = "user_not_exists"


class CodeMismatch(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Неверный проверочный код"
    code = "code_mismatch"


class EmptyUserSocials(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Должен присутствовать хотя бы один идентификатор"
    code = "empty_user_socials"
