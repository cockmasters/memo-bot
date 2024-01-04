from core.exceptions import BusinessException
from starlette import status


class NoteExists(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Записка {title} существует"
    code = "note_exists"


class NoteNotExists(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    detail_template = "Записки не существует"
    code = "note_not_exists"
