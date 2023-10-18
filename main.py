from fastapi import FastAPI

from walmart_alert_api.api.alert import router as alerts_router

app = FastAPI()
app.include_router(alerts_router)


@app.get("/")
async def health():
    return "ok"
