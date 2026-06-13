import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwODU1NTM1LCJpYXQiOjE3ODA4MTk1MzUsImp0aSI6ImNiZmMzZThmZjBkYjQ4NGZiMzBhMzgxYjJmNWJjNTk0IiwidXNlcl9pZCI6MzUsInJlZnJlc2hfanRpIjoiODMxYzQ1MDMyODc0NDY3NDk3ZWJiODM3YmM3YTczNGMifQ.vniWt4yZhxVTwIhPHeRI8_Z8uGMet0ydQe-TMc72e_Y"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDkwNTkzNSwiaWF0IjoxNzgwODE5NTM1LCJqdGkiOiI4MzFjNDUwMzI4NzQ0Njc0OTdlYmI4MzdiYzdhNzM0YyIsInVzZXJfaWQiOjM1fQ.Z11gPxE5XoxZ0T5G2RsALAS05-F8me506TyRwivkOIU"
@pytest.fixture(scope="session")
def authenticated_page():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)

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