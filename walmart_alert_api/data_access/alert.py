from fastapi import HTTPException
from pydantic import BaseModel

from walmart_alert_api.data_access.client import db_client
from walmart_alert_api.models.alert import Alert


class CustomErrorModel(BaseModel):
    custom_message: str


def insert_alert(alert: Alert):
    cur = db_client.cursor()
    cur.execute(
        f"""
        INSERT INTO alert VALUES 
            ('{alert.alert_id}',
            '{alert.service_id}',
            '{alert.service_name}',
            '{alert.model}',
            '{alert.alert_type}',
            '{alert.alert_ts}',
            '{alert.severity}',
            '{alert.team_slack}'
        );
    """
    )
    db_client.commit()
    return alert


def get_alerts(service_id: str, start_ts: str, end_ts: str):
    cur = db_client.cursor()
    res = cur.execute(
        f"""
        SELECT * FROM alert
        WHERE service_id = '{service_id}'
        AND alert_ts >= {start_ts}
        AND alert_ts <= {end_ts}
        ;
    """
    )
    alerts = res.fetchall()
    alerts_list = []
    service_name = ""
    for alert in alerts:
        service_name = alert[2]
        alerts_list.append(
            Alert(
                alert_id=alert[0],
                service_id=alert[1],
                service_name=alert[2],
                model=alert[3],
                alert_type=alert[4],
                alert_ts=alert[5],
                severity=alert[6],
                team_slack=alert[7],
            ).model_dump()
        )

    return alerts_list, service_name
