import json

import pytest
from fastapi.testclient import TestClient

from main import app
from tests.data.alert_data import (
    ALERTS_SERVICE_A,
    ALERTS_SERVICE_X,
    SERVICE_ID_A,
    SERVICE_ID_X,
)
from walmart_alert_api.data_access.alert import delete_alert

client = TestClient(app)


class TestAlerts:
    def after_all(self):
        for test_alert in ALERTS_SERVICE_X + ALERTS_SERVICE_A:
            delete_alert(test_alert["service_id"])

    @pytest.fixture(scope="class", autouse=True)
    def before_all(self, request):
        # before all
        for test_alert in ALERTS_SERVICE_X:
            client.post(url="/alerts", content=json.dumps(test_alert))

        # after all
        request.addfinalizer(self.after_all)

    def test_get_alerts_all(self):
        # test getting everything in range
        start_ts = 1
        end_ts = 6000
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 5

    def test_get_alerts_edge(self):
        # test case where start or end is equal to ts
        start_ts = 1000
        end_ts = 5000
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 5

    def test_get_alerts_end_ts(self):
        # test cutting off alerts by end_ts
        start_ts = 1000
        end_ts = 4999
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 4

        end_ts = 3999
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 3

        end_ts = 2999
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 2

        end_ts = 1999
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 1

        end_ts = 999
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 0

    def test_get_alerts_start_ts(self):
        # test cutting off alerts by end_ts
        start_ts = 1001
        end_ts = 6000
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 4

        start_ts = 2001
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 3

        start_ts = 3001
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 2

        start_ts = 4001
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 1

        start_ts = 5001
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 0

    def test_get_alerts_for_specific_service(self):
        # test that it only retrieves alerts for the specified service
        for alert in ALERTS_SERVICE_A:
            client.post(url="/alerts", content=json.dumps(alert))

        start_ts = 1000
        end_ts = 5000
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 5

        response = client.get(
            f"/alerts?service_id={SERVICE_ID_A}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 1

    def test_post_dup_alert_id(self):
        # test that you cant add duplicate alert ids
        dup_alert = ALERTS_SERVICE_X[0]

        response = client.post(url="/alerts", content=json.dumps(dup_alert))
        assert response.status_code == 400
        assert response.json()["alert_id"] == "x_1"
        assert response.json()["error"] != ""

        # check that it truly was not added
        start_ts = 1000
        end_ts = 5000
        response = client.get(
            f"/alerts?service_id={SERVICE_ID_X}&start_ts={start_ts}&end_ts={end_ts}"
        )
        assert response.status_code == 200
        assert len(response.json()["alerts"]) == 5
