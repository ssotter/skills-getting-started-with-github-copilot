import sys
import pathlib
import urllib.parse

# Ensure `src` is importable
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activities from the seed data
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister_flow():
    import sys
    import pathlib
    import urllib.parse

    # Ensure `src` is importable
    ROOT = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT / "src"))

    from fastapi.testclient import TestClient
    from app import app

    client = TestClient(app)


    def test_get_activities():
        resp = client.get("/activities")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        # Expect some known activities from the seed data
        assert "Chess Club" in data
        assert "Programming Class" in data


    def test_signup_and_unregister_flow():
        activity = "Chess Club"
        email = "pytest-user@example.com"

        # Ensure email is not already present
        resp = client.get("/activities")
        assert resp.status_code == 200
        participants = resp.json()[activity]["participants"]
        if email in participants:
            # If a previous run left state, remove it first
            client.post(f"/activities/{urllib.parse.quote(activity)}/unregister?email={urllib.parse.quote(email)}")

        # Signup should succeed
        signup = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
        assert signup.status_code == 200
        assert "Signed up" in signup.json().get("message", "")

        # Participant should appear in activity list
        resp = client.get("/activities")
        assert resp.status_code == 200
        participants = resp.json()[activity]["participants"]
        assert email in participants

        # Signing up again should fail (duplicate)
        dup = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
        assert dup.status_code == 400

        # Unregister should succeed
        unreg = client.post(f"/activities/{urllib.parse.quote(activity)}/unregister?email={urllib.parse.quote(email)}")
        assert unreg.status_code == 200
        assert "Unregistered" in unreg.json().get("message", "")

        # Participant should be gone
        resp = client.get("/activities")
        participants = resp.json()[activity]["participants"]
        assert email not in participants