from pytest_bdd import scenario
from steps.user_management_steps import *

@scenario(
    "../features/user_management.feature",
    "Create and Verify User"
)
def test_create_user():
    pass


@scenario(
    "../features/user_management.feature",
    "New user with duplicate mobile number"
)
def test_duplicate_mobile():
    pass

@scenario(
    "../features/user_management.feature",
    "New user with duplicate email"
)
def test_duplicate_email():
    pass

@scenario(
    "../features/user_management.feature",
    "New user without email id"
)
def test_user_without_email():
    pass
