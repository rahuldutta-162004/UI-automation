import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNzUzNjY4LCJpYXQiOjE3ODA3MTc2NjgsImp0aSI6IjE2ZGEwMWUyMDhjYTQzNGQ4OWQ4NjMxOTdjZjQ3NmQwIiwidXNlcl9pZCI6MzUsInJlZnJlc2hfanRpIjoiMDY5OWFkNjdjNTY1NDBiZDhlYjJmODg5MmI3ZDZiMGYifQ.J6HX4f8P-yn6lmbcMd3MjsFp25ghHkpWOXSlRRaHiSk"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDgwNDA2OCwiaWF0IjoxNzgwNzE3NjY4LCJqdGkiOiIwNjk5YWQ2N2M1NjU0MGJkOGViMmY4ODkyYjdkNmIwZiIsInVzZXJfaWQiOjM1fQ.EyEOoCZqKu15unfHEddb7ZhzeM-TGpTzoxx8Bh9MSQE"
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