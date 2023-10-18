from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.data_access.alert import get_alerts_dynamic
from app.models.custom_exception import AlertException

router = APIRouter(
    prefix="/v2/alerts",
    tags=["alerts", "v2"],
)


@router.get("")
async def read_alert(service_id: str = "", start_ts: int = None, end_ts: int = None):
    try:
        alerts_dict = get_alerts_dynamic(service_id, start_ts, end_ts)
        response = {"num_services": len(alerts_dict), "services": []}
        for key, value in alerts_dict.items():
            if len(value):
                response["services"].append(
                    {
                        "service_id": key,
                        "service_name": value[0]["service_name"],
                        "alerts": value,
                    }
                )

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
