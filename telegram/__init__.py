from config import backend_settings

from backend_request.api import BackendApi

api = BackendApi(backend_settings.BASE_URL)
