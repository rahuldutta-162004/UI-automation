from pytest_bdd import given, when, then
from datetime import datetime
import logging

from POM.view_modify_records_page import ViewModifyRecordsPage

logger = logging.getLogger(__name__)


@given("user is authenticated for MDM", target_fixture="page")
def user_authenticated_for_mdm(authenticated_page):
    return authenticated_page


@when("user opens view modify records from control panel")
def open_view_modify_records(page):
    vmr_page = ViewModifyRecordsPage(page)
    vmr_page.open_view_modify_records()


@then("the error message of invalid request should come")
def verify_invalid_request_error(page):
    vmr_page = ViewModifyRecordsPage(page)
    vmr_page.verify_invalid_request_error()
    logger.info("Invalid request error displayed")


@when("user edits the item description online")
def edit_item_description_online(page, test_data):

    description = (
        f"itemdesc{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    test_data["item_description"] = description

    vmr_page = ViewModifyRecordsPage(page)
    vmr_page.edit_item_description(description)

    logger.info(
        "Updated item description : %s",
        description
    )


@when("user edit the configuration code and save")
def edit_configuration_code_and_save(page):

    vmr_page = ViewModifyRecordsPage(page)

    vmr_page.edit_configuration_code(
        "configcode123"
    )

    logger.info("Configuration code updated")


@then("the updated item description should be visible in task status")
def verify_updated_item_description_in_task_status(
    page,
    test_data
):

    vmr_page = ViewModifyRecordsPage(page)

    vmr_page.verify_task_status(
        test_data["item_description"]
    )

    logger.info(
        "Verified updated item description in task status"
    )