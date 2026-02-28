from fastapi.testclient import TestClient

from some_logo.gui import app

client = TestClient(app)


def test_static_files() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Some Logo Generator" in response.text


def test_api_generate_success() -> None:
    payload = {
        "text": "test",
        "mode": "square",
        "add_frame": True,
        "add_text": False,
        "random_colors": False,
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    assert "image/svg+xml" in response.headers["content-type"]
    assert "<svg" in response.text


def test_api_generate_missing_text() -> None:
    response = client.post("/api/generate", json={})
    assert response.status_code == 422
