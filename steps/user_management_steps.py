from pytest_bdd import given, when, then
from datetime import datetime
import logging

from POM.user_management_page import (
    UserManagementPage
)

logger = logging.getLogger(__name__)


@given(
    "user is authenticated",
    target_fixture="page"
)
def user_authenticated(
    authenticated_page
):
    return authenticated_page


@when("user creates a new user")
def create_user(
    page,
    test_data
):

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    email = f"testuser{timestamp}"
    mobile = f"91{timestamp[-10:]}"

    test_data["email"] = (
        f"{email}@gmail.com"
    )

    user_page = UserManagementPage(
        page
    )

    user_page.create_user(
        "Pranav",
        "Dutta",
        mobile,
        email
    )

    logger.info(
        "User created: %s",
        email
    )


@when(
    "user creates a new user with duplicate mobile number"
)
def duplicate_mobile(
    page,
    test_data
):

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    email = f"testuser{timestamp}"

    user_page = UserManagementPage(
        page
    )

    user_page.create_user(
        "Pranav",
        "Dutta",
        "9322123482",
        email
    )

@when("user creates a new user without email")
def create_user_without_email(page):
    pass

@then("the user creation should fail")
def validate_user_creation_failure(page):
    pass

@then(
    "the user creation should fail with duplicate mobile error"
)
def validate_duplicate_mobile(
    page
):

    user_page = UserManagementPage(
        page
    )

    user_page.verify_failed_user_creation()


@when(
    "user creates a new user with duplicate email"
)
def duplicate_email(
    page
):

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    mobile = f"91{timestamp[-10:]}"

    user_page = UserManagementPage(
        page
    )

    user_page.create_user(
        "Pranav",
        "Dutta",
        mobile,
        "rdlipika16"
    )


@when(
    "user searches for the created user"
)
def search_user(
    page,
    test_data
):

    user_page = UserManagementPage(
        page
    )

    user_page.search_user(
        test_data["email"]
    )


@then(
    "the user should be visible in the user management table"
)
def validate_user(
    page,
    test_data
):

    user_page = UserManagementPage(
        page
    )

    user_page.verify_user_exists(
        test_data["email"]
    )

    logger.info(
        "User verified successfully"
    )