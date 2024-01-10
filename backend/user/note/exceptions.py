from core.exceptions import BusinessException
from starlette import status


class NoteNotExists(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    detail_template = "Записки не существует"
    code = "note_not_exists"
