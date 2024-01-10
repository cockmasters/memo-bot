from config import backend_settings

from ..api import BackendApi

api = BackendApi(backend_settings.BASE_URL)
