from pytest_bdd import given, when, then, parsers
import logging

from POM.sales_clearance_portal_page import (
    SalesClearancePortalPage
)

logger = logging.getLogger(__name__)


@given("user is authenticated for Sales",
       target_fixture="page")
def user_authenticated_for_sales(
    authenticated_page
):
    return authenticated_page


@when("user opens the sales clearance portal and save")
def open_sales_clearance_portal(
    page,
    test_data
):

    sales_page = SalesClearancePortalPage(
        page
    )

    sales_page.open_sales_clearance_portal()

    sls_ord_line_id = (
        sales_page.get_first_sales_order_line_id()
    )

    test_data[
        "sls_ord_line_id"
    ] = sls_ord_line_id

    logger.info(
        "First row Sls Ord Line Id: %s",
        sls_ord_line_id
    )

    sales_page.click_scheduling_and_save()

    logger.info(
        "Opened Sales Clearance Portal and clicked Save"
    )


@then(
    "the saved sales order line should be visible in Design"
)
def verify_saved_sales_order_line_in_design(
    page,
    test_data
):

    sales_page = SalesClearancePortalPage(
        page
    )

    sales_page.open_design_tab()

    design_ids = (
        sales_page.get_design_sales_order_line_ids()
    )

    sls_ord_line_id = test_data[
        "sls_ord_line_id"
    ]

    assert (
        sls_ord_line_id in design_ids
    ), (
        f"Sls Ord Line Id "
        f"{sls_ord_line_id} not found in Design. "
        f"Visible values: {design_ids}"
    )

    logger.info(
        "Verified Sls Ord Line Id %s is visible in Design",
        sls_ord_line_id
    )


@when(
    parsers.parse(
        'user filters by sales order line "{sales_order_line}"'
    )
)
def filter_by_sales_order_line(
    page,
    sales_order_line
):

    sales_page = SalesClearancePortalPage(
        page
    )

    sales_page.filter_by_sales_order_line(
        sales_order_line
    )

    logger.info(
        "Selected sales order line filter: %s",
        sales_order_line
    )


@then(
    parsers.parse(
        'sales order line "{sales_order_line}" '
        'should be selected in the filter'
    )
)
def verify_sales_order_line_filter_selected(
    page,
    sales_order_line
):

    sales_page = SalesClearancePortalPage(
        page
    )

    sales_page.verify_filter_selected(
        sales_order_line
    )

    logger.info(
        "Verified sales order line filter is selected: %s",
        sales_order_line
    )