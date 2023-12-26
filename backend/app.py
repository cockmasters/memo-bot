import uvicorn
from backend.config import settings
from backend.core.exceptions import BusinessException
from backend.healthcheck.routes import router as healthcheck_router
from backend.note.routes import router as note_router
from backend.user.routes import router as user_router
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title=settings.app_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(healthcheck_router, tags=["Healthcheck"], prefix="/api")
app.include_router(user_router, tags=["Organisation"], prefix="/api/user")
app.include_router(note_router, tags=["Organisation"], prefix="/api/note")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    # TODO: добавить логирование ошибки

    return JSONResponse(
        {"code": "internal_server_error", "detail": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(exc.to_json(), status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
