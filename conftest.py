import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NjExMjkzLCJpYXQiOjE3ODQ2MTA2OTMsImp0aSI6ImMzMDkzYzdmN2YzNDQ5NjZiY2QxZTY2Mjc5ZjFlYjFkIiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6ImY0MWM4NDQyZmMyODRkMzJiMDZiZDJmMzk0NjA5ODE0In0.Ipy0QVdJc7Jocy7x3qxsG9L2dIfYniMnsh0oxcf_x38"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NDY5NzA5MywiaWF0IjoxNzg0NjEwNjkzLCJqdGkiOiJmNDFjODQ0MmZjMjg0ZDMyYjA2YmQyZjM5NDYwOTgxNCIsInVzZXJfaWQiOjM1LCJpc19zc28iOnRydWUsInNzb19wcm92aWRlcl91c2VyX2lkIjoiMzY3YmQwMzgtNGI5MC00NDc3LWFiODktZGM4ZWNiYjc4MTc5Iiwic3NvX2NsaWVudF9pZCI6MX0._NVid7Ie7gO1zYUrTApORm1gDNXz10JvNmNRayTxVqQ"
@pytest.fixture(scope="session")
def authenticated_page():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

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
