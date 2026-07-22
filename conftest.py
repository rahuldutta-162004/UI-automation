import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzE3NzE0LCJpYXQiOjE3ODQ2OTczNTMsImp0aSI6IjI1YjljMjM3NmNiMjQzNWJiZTg3Njg1NzJlNjE1MTQ4IiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6IjFiMzc2MTM2ZTMzZjQxZThhYmQ5ZTkxN2JiMWE0ZWIzIn0.gvmgXRFQpkqHGgO7Zzz_BubjBcnl4wn0iyTxPXcPanQ"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NDc4Mzc1MywiaWF0IjoxNzg0Njk3MzUzLCJqdGkiOiIxYjM3NjEzNmUzM2Y0MWU4YWJkOWU5MTdiYjFhNGViMyIsInVzZXJfaWQiOjM1LCJpc19zc28iOnRydWUsInNzb19wcm92aWRlcl91c2VyX2lkIjoiMzY3YmQwMzgtNGI5MC00NDc3LWFiODktZGM4ZWNiYjc4MTc5Iiwic3NvX2NsaWVudF9pZCI6MX0.i5nzcFeOkMBeyvQksowenUXtIVSbSbAPiTduJHdTrGg"

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
