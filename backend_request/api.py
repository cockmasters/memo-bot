from functools import partial
from typing import Any, Optional, Protocol, Type, TypeVar

from backend_request.schemas import CreateUserResponse, GetUserProfileResponse, Note, NoteCreateResponse
from httpx import AsyncClient, HTTPError


class SupportsAsdict(Protocol):
    def asdict(self) -> dict[str, Any]:
        pass


RESPONSE = TypeVar("RESPONSE", bound=SupportsAsdict)


class BackendApi:
    class Error(Exception):
        def __init__(self, method: str, status_code: Optional[int] = None):
            self.method = method
            self.status_code = status_code

        def __str__(self):
            error = self.status_code if self.status_code else "Not connected"
            return f"BackendApiError: {error}"

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def request(
        self,
        method: str,
        path: str,
        data: SupportsAsdict,
        response_type: Type[RESPONSE],
    ) -> RESPONSE | list[RESPONSE]:
        try:
            async with AsyncClient() as client:
                response = await client.request(method=method, url=f"{self.base_url}{path}", json=data.asdict())
                response.raise_for_status()
        except HTTPError as exc:
            status_code = response.status_code if response else None
            raise BackendApi.Error(method, status_code) from exc
        data = response.json()
        if isinstance(data, list):
            return [response_type(el) for el in data]
        return response_type(**response.json())

    create_user = partial(request, method="POST", path="/api/user/", response_type=CreateUserResponse)
    get_profile = partial(
        request,
        method="GET",
        path="/api/user/{tg_id}/",
        response_type=GetUserProfileResponse,
    )
    create_note = partial(request, method="POST", path="/api/note/", response_type=NoteCreateResponse)
    get_notes_all = partial(
        request,
        method="GET",
        path="/api/user/{user_id}/note/all/",
        response_type=list[Note],
    )
    filter_notes = partial(
        request,
        method="POST",
        path="/api/user/{user_id}/note/filter/",
        response_type=list[Note],
    )
    edit_note = partial(request, method="PUT", path="/api/note/{note_id}/", response_type=Note)
    delete_note = partial(
        request,
        method="DELETE",
        path="/api/user/{user_id}/note/{note_id}/",
        response_type=None,
    )
