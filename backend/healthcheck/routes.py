from fastapi import APIRouter, status

router = APIRouter()


@router.get("/healthcheck", status_code=status.HTTP_204_NO_CONTENT)
async def healthcheck():
    return
