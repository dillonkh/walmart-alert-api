class AlertException(Exception):
    def __init__(
        self, status_code: str, alert_id: str, service_id: str, error_message: str
    ):
        self.status_code = status_code
        self.alert_id = alert_id
        self.service_id = service_id
        self.error_message = error_message
