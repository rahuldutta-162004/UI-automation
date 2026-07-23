import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = ""eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzkzMTE3LCJpYXQiOjE3ODQ3ODk1MDQsImp0aSI6IjgyNTEyYjQyMjAxZjQxY2E5YTMzZjY4MjllYTg0N2YzIiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6ImJjZTAyNmYyM2Q5MzQxMjhhOWE2OTg0NjBlMjRjMWIyIn0.S7EcCZlJzZRLA9L6KX5B3ejhdR5qlaw0O83RtvD2zWw
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzkzMTE3LCJpYXQiOjE3ODQ3ODk1MDQsImp0aSI6IjgyNTEyYjQyMjAxZjQxY2E5YTMzZjY4MjllYTg0N2YzIiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6ImJjZTAyNmYyM2Q5MzQxMjhhOWE2OTg0NjBlMjRjMWIyIn0.S7EcCZlJzZRLA9L6KX5B3ejhdR5qlaw0O83RtvD2zWw"

@pytest.fixture(scope="session")
def authenticated_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()
        page = context.new_page()

        page.goto("https://sentinel.oritiq.org/login")

        page.evaluate(
            """
            ([access, refresh]) => {
                localStorage.setItem("access_token", access);
                localStorage.setItem("refresh_token", refresh);
            }
            """,
            [ACCESS_TOKEN, REFRESH_TOKEN]
        )
        
        page.reload()
        yield page
       

        browser.close()
@pytest.fixture
def test_data():
    return {}


@pytest.fixture(autouse=True)
def reload_after_scenario(authenticated_page):
    """Reload the authenticated page after each test/scenario to ensure clean state."""
    yield
    try:
        authenticated_page.reload()
        authenticated_page.wait_for_load_state("networkidle")
    except Exception:
        # best-effort reload; don't fail the test because of reload errors
        pass
