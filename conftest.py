import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzkwMTA0LCJpYXQiOjE3ODQ3ODk1MDQsImp0aSI6IjFhNDcxZDM1OTJhYjQ2ZWViYTJkYzc4OGJkNDMzZDFkIiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6ImJjZTAyNmYyM2Q5MzQxMjhhOWE2OTg0NjBlMjRjMWIyIn0.5qX9U30sFQC0SWPyR9Fqz2Mvy6HjqrixyNr_Hm10NFI"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NDg3NTkwNCwiaWF0IjoxNzg0Nzg5NTA0LCJqdGkiOiJiY2UwMjZmMjNkOTM0MTI4YTlhNjk4NDYwZTI0YzFiMiIsInVzZXJfaWQiOjM1LCJpc19zc28iOnRydWUsInNzb19wcm92aWRlcl91c2VyX2lkIjoiMzY3YmQwMzgtNGI5MC00NDc3LWFiODktZGM4ZWNiYjc4MTc5Iiwic3NvX2NsaWVudF9pZCI6MX0.5Z4J7oSQeN7o1D4KwPKUlsSTdFjIudV7ns4FYDGl10w"

@pytest.fixture(scope="session")
def authenticated_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

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
