import sqlite3

from fastapi import status
from pydantic import BaseModel

from app.models.alert import Alert
from app.models.custom_exception import AlertException


class CustomErrorModel(BaseModel):
    custom_message: str


DB_NAME = "walmart-exam.db"


def delete_alert(service_id: str):
    db_client = sqlite3.connect(DB_NAME)
    cur = db_client.cursor()
    cur.execute(
        f"""
        DELETE FROM alert
        WHERE service_id = ?;
        """,
        (service_id,),
    )
    db_client.commit()
    return service_id


def insert_alert(alert: Alert):
    try:
        db_client = sqlite3.connect(DB_NAME)
        cur = db_client.cursor()
        cur.execute(
            """
            INSERT INTO alert VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                alert.alert_id,
                alert.service_id,
                alert.service_name,
                alert.model,
                alert.alert_type,
                alert.alert_ts,
                alert.severity,
                alert.team_slack,
            ),
        )
        db_client.commit()
        return alert
    except sqlite3.IntegrityError as e:
        raise AlertException(
            status_code=status.HTTP_400_BAD_REQUEST,
            alert_id=alert.alert_id,
            service_id=alert.service_id,
            error_message=str(e),
        )
    except sqlite3.OperationalError as e:
        raise AlertException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            alert_id=alert.alert_id,
            service_id=alert.service_id,
            error_message=str(e),
        )


def get_alerts(service_id: str, start_ts: str, end_ts: str):
    db_client = sqlite3.connect(DB_NAME)
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


def get_alerts_dynamic(service_id: str = "", start_ts: str = None, end_ts: str = None):
    db_client = sqlite3.connect(DB_NAME)
    cur = db_client.cursor()

    # dynamically build the query based on which params are passed
    if not service_id and start_ts is None and end_ts is None:
        raise AlertException(
            status_code=status.HTTP_400_BAD_REQUEST,
            alert_id=None,
            service_id=service_id,
            error_message="Input error, at least one of the following must be defined: 'service_id', 'start_ts', 'end_ts'",
        )

    query = "SELECT * FROM alert WHERE"
    params = []

    if service_id:
        query += " service_id = ? AND"
        params.append(service_id)

    if start_ts is not None:
        query += " alert_ts >= ? AND"
        params.append(start_ts)

    if end_ts is not None:
        query += " alert_ts <= ? AND"
        params.append(end_ts)

    # Remove the trailing "AND" if it exists
    query = query.rstrip(" AND") + ";"

    res = cur.execute(query, params)
    alerts = res.fetchall()

    alerts_dict = {}
    for alert in alerts:
        if alert[1] not in alerts_dict:
            alerts_dict[alert[1]] = []

        alerts_dict[alert[1]].append(
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

    return alerts_dict
