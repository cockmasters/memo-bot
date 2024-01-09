from dataclasses import asdict, is_dataclass
from functools import partialmethod
from typing import Optional, Type, TypeVar, get_args

from backend_request.schemas import AuthKey, CreateUserResponse, GetUserProfileResponse, Note, NoteCreateResponse
from httpx import AsyncClient, HTTPError, HTTPStatusError

RESPONSE = TypeVar("RESPONSE")


class BackendApi:
    class Error(Exception):
        def __init__(self, method: str, status_code: Optional[int] = None, message: Optional[str] = None):
            self.method = method
            self.status_code = status_code
            self.message = message

        def __str__(self):
            error = self.status_code if self.status_code else "Not connected"
            return f"BackendApiError on {self.method}: {error}"

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def request(
        self,
        method: str,
        path: str,
        response_type: Type[RESPONSE],
        data: Optional = None,
        **path_params,
    ) -> RESPONSE | list[RESPONSE]:
        try:
            path = path.format(**path_params)
            data = asdict(data) if is_dataclass(data) else None
            async with AsyncClient() as client:
                response = await client.request(method=method, url=f"{self.base_url}{path}", json=data)
                response.raise_for_status()
        except HTTPStatusError as exc:
            raise BackendApi.Error(
                method=method, status_code=response.status_code, message=response.json()["detail"]
            ) from exc
        except HTTPError as exc:
            status_code = response.status_code if response else None
            raise BackendApi.Error(method, status_code) from exc
        data = response.json()
        if isinstance(data, list):
            subtype = get_args(response_type)[0]
            return [subtype(**el) for el in data]
        return response_type(**response.json())

    create_user = partialmethod(request, method="POST", path="/api/user/", response_type=CreateUserResponse)
    get_profile = partialmethod(
        request,
        method="GET",
        path="/api/user/{social_id}/",
        response_type=GetUserProfileResponse,
    )
    create_note = partialmethod(
        request, method="POST", path="/api/user/{user_id}/note/", response_type=NoteCreateResponse
    )
    get_notes_all = partialmethod(
        request,
        method="GET",
        path="/api/user/{user_id}/note/all/",
        response_type=list[Note],
    )
    filter_notes = partialmethod(
        request,
        method="POST",
        path="/api/user/{user_id}/note/filter/",
        response_type=list[Note],
    )
    edit_note = partialmethod(request, method="PUT", path="/api/note/{note_id}/", response_type=Note)
    delete_note = partialmethod(
        request,
        method="DELETE",
        path="/api/user/{user_id}/note/{note_id}/",
        response_type=None,
    )
    get_auth_key = partialmethod(request, method="GET", path="/api/user/{user_id}/auth/key/", response_type=AuthKey)
    link_account = partialmethod(request, method="POST", path="/api/user/{user_id}/link/")
