import pytest
from playwright.sync_api import sync_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzkzNzM0LCJpYXQiOjE3ODQ3OTMxMzQsImp0aSI6ImEyYTAzN2RhZDI5MDRkNmNiMTdlMDczMGRkMTA5NDVlIiwidXNlcl9pZCI6MzUsImlzX3NzbyI6dHJ1ZSwic3NvX3Byb3ZpZGVyX3VzZXJfaWQiOiIzNjdiZDAzOC00YjkwLTQ0NzctYWI4OS1kYzhlY2JiNzgxNzkiLCJzc29fY2xpZW50X2lkIjoxLCJyZWZyZXNoX2p0aSI6IjQ5MWM3YThkMWRjNDRjOGZhOGZiMjJlMTlhMzU1NTZmIn0.1Lih8XzLmzVdo9bRocXAUEWqgEf3QQnfcsY-VcP6R1s"
REFRESH_TOKEN ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NDg3OTUzNCwiaWF0IjoxNzg0NzkzMTM0LCJqdGkiOiI0OTFjN2E4ZDFkYzQ0YzhmYThmYjIyZTE5YTM1NTU2ZiIsInVzZXJfaWQiOjM1LCJpc19zc28iOnRydWUsInNzb19wcm92aWRlcl91c2VyX2lkIjoiMzY3YmQwMzgtNGI5MC00NDc3LWFiODktZGM4ZWNiYjc4MTc5Iiwic3NvX2NsaWVudF9pZCI6MX0.T_X05yPl4PpHy9zGrMN28KkhoSiv90VVZuCS4sqRex8"

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
