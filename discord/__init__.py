from config import settings

from ..api import BackendApi

api = BackendApi(settings.BASE_URL)
