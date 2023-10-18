from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.alert import router as v1_router
from app.api.v2.alert import router as v2_router
from app.models.custom_exception import AlertException

app = FastAPI()
app.include_router(v1_router)
app.include_router(v2_router)


@app.exception_handler(AlertException)
async def alert_exception_handler(request: Request, e: AlertException):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "success": False,
            "alert_id": e.alert_id,
            "service_id": e.service_id,
            "error": e.error_message,
        },
    )


@app.get("/")
async def health():
    return "ok"
