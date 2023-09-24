from abc import ABC, abstractmethod
from typing import Mapping, Optional

from fastapi import status


class BusinessException(ABC, Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: Optional[str] = None

    @property
    @abstractmethod
    def detail_template(self) -> str:
        pass

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    def __init__(self, **kwargs):
        self.detail = self.detail_template.format(**kwargs)

    def to_json(self) -> Mapping:
        return {"code": self.code, "detail": self.detail}
