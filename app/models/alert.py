from pydantic import BaseModel


class Alert(BaseModel):
    alert_id: str
    service_id: str
    service_name: str
    model: str
    alert_type: str
    alert_ts: int
    severity: str
    team_slack: str
