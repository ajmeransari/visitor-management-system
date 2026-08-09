from app import app


def test_app_exists():
    assert app is not None


def test_home_page_redirects_to_login():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 302
    assert "/auth/login" in response.location