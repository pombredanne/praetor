from starlette.testclient import TestClient
from praetor.cli.webserver import app


tc = TestClient(app)


class TestGetFlows:
    def test_returns_list(self):
        res = tc.get("/flows")
        assert isinstance(res.data, list)
