from functools import partialmethod
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
            return f"BackendApiError on {self.method}: {error}"

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def request(
        self,
        method: str,
        path: str,
        response_type: Type[RESPONSE],
        data: Optional[SupportsAsdict] = None,
        **path_params,
    ) -> RESPONSE | list[RESPONSE]:
        try:
            path = path.format(**path_params)
            data = data.asdict() if data else None
            async with AsyncClient() as client:
                response = await client.request(method=method, url=f"{self.base_url}{path}", json=data)
                response.raise_for_status()
        except HTTPError as exc:
            status_code = response.status_code if response else None
            raise BackendApi.Error(method, status_code) from exc
        data = response.json()
        if isinstance(data, list):
            return [response_type(el) for el in data]
        return response_type(**response.json())

    create_user = partialmethod(request, method="POST", path="/api/user/", response_type=CreateUserResponse)
    get_profile = partialmethod(
        request,
        method="GET",
        path="/api/user/{social_id}/",
        response_type=GetUserProfileResponse,
    )
    create_note = partialmethod(request, method="POST", path="/api/note/", response_type=NoteCreateResponse)
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
