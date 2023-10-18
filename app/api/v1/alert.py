from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.data_access.alert import get_alerts, insert_alert
from app.models.alert import Alert
from app.models.custom_exception import AlertException

router = APIRouter(
    prefix="/v1/alerts",
    tags=["alerts", "v1"],
)


class CustomErrorModel(BaseModel):
    custom_message: str


@router.post("")
async def write_alert(alert: Alert):
    try:
        inserted_alert = insert_alert(alert)

        return {"alert_id": inserted_alert.alert_id, "error": ""}
    except AlertException as e:
        raise e
    except Exception as e:
        raise AlertException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            alert_id=alert.alert_id,
            service_id=alert.service_id,
            error_message=str(e),
        )


@router.get("")
async def read_alert(service_id: str, start_ts: int, end_ts: int):
    try:
        alerts, service_name = get_alerts(service_id, start_ts, end_ts)
        response = {
            "service_id": service_id,
            "service_name": service_name,
            "alerts": alerts,
        }
        return JSONResponse(content=response)
    except AlertException as e:
        raise e
    except Exception as e:
        raise AlertException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            alert_id=None,
            service_id=service_id,
            error_message=str(e),
        )
