from starlette import status

from core.exceptions import BusinessException


class NoteExists(BusinessException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail_template = "Записка {title} существует"
    code = "note_exists"
