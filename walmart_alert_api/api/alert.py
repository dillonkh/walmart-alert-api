import json

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from walmart_alert_api.data_access.alert import get_alerts, insert_alert
from walmart_alert_api.models.alert import Alert

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
)


class CustomErrorModel(BaseModel):
    custom_message: str


@router.post("")
async def write_alert(alert: Alert):
    try:
        inserted_alert = insert_alert(alert)

        return {"alert_id": inserted_alert.alert_id, "error": ""}
    except Exception as e:
        error_response = {"alert_id": alert.alert_id, "error": str(e)}
        return JSONResponse(content=error_response, status_code=400)


@router.get("")
async def read_alert(service_id: str, start_ts: str, end_ts: str):
    alerts, service_name = get_alerts(service_id, start_ts, end_ts)
    response = {"service_id": service_id, "service_name": service_name, "alerts": alerts}
    return JSONResponse(content=response)
