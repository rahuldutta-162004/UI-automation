from playwright.sync_api import expect


class SalesClearancePortalPage:

    def __init__(self, page):
        self.page = page

    # ==================
    # Locators
    # ==================

    @property
    def sales_portal_link(self):
        return self.page.get_by_role(
            "link",
            name="Sales Clearance Portal"
        )

    @property
    def first_sales_row(self):
        return self.page.locator(
            "tbody tr.ant-table-row"
        ).first

    @property
    def save_button(self):
        return self.page.locator(
            "button[data-slot='button'].primary-gradient"
        )

    @property
    def design_tab(self):
        return self.page.locator(
            "button[role='tab']",
            has_text="Design"
        )

    @property
    def filter_icon(self):
        return self.page.locator(
            "#sales_order_line_id > .flex > .flex-1 > "
            ".ant-table-filter-column > .ant-dropdown-trigger > "
            ".anticon > svg"
        )

    # ==================
    # Actions
    # ==================

    def open_sales_clearance_portal(self):

        self.sales_portal_link.wait_for(
            state="visible",
            timeout=10000
        )

        self.sales_portal_link.click()

        self.page.wait_for_load_state(
            "networkidle"
        )

    def get_first_sales_order_line_id(self):

        self.first_sales_row.wait_for(
            state="visible",
            timeout=10000
        )

        sales_order_id = self.first_sales_row.locator(
            "#sales_order_line_id"
        )

        sales_order_id.wait_for(
            state="visible",
            timeout=10000
        )

        return sales_order_id.inner_text().strip()

    def click_scheduling_and_save(self):

        scheduling = self.first_sales_row.locator(
            "#clearance_history"
        ).get_by_text(
            "Scheduling",
            exact=True
        ).first

        scheduling.wait_for(
            state="visible",
            timeout=10000
        )

        scheduling.click()

        cleared_for_radio = self.page.locator(
            "div.flex.gap-2.p-3",
            has_text="Cleared For"
        ).locator(
            "input[type=radio]"
        ).first

        cleared_for_radio.wait_for(
            state="visible",
            timeout=10000
        )

        cleared_for_radio.evaluate(
            """
            element => {
                element.click();
                element.checked = true;
                element.dispatchEvent(
                    new Event("input", { bubbles: true })
                );
                element.dispatchEvent(
                    new Event("change", { bubbles: true })
                );
            }
            """
        )

        expect(self.save_button).to_be_visible()
        expect(self.save_button).to_be_enabled()

        self.save_button.click()

        self.page.wait_for_load_state(
            "networkidle"
        )

    def open_design_tab(self):

        self.design_tab.wait_for(
            state="visible",
            timeout=10000
        )

        self.design_tab.click()

        self.page.wait_for_load_state(
            "networkidle"
        )

    def get_design_sales_order_line_ids(self):

        self.page.locator(
            "tbody tr.ant-table-row"
        ).first.wait_for(
            state="visible",
            timeout=10000
        )

        return [
            value.strip()
            for value in self.page.locator(
                "tbody tr.ant-table-row #sales_order_line_id"
            ).all_inner_texts()
        ]

    def filter_by_sales_order_line(
        self,
        sales_order_line
    ):

        self.filter_icon.wait_for(
            state="visible",
            timeout=10000
        )

        self.filter_icon.click()

        checkbox = self.page.get_by_role(
            "checkbox",
            name=sales_order_line
        )

        checkbox.wait_for(
            state="visible",
            timeout=10000
        )

        checkbox.check()

    def verify_filter_selected(
        self,
        sales_order_line
    ):

        checkbox = self.page.get_by_role(
            "checkbox",
            name=sales_order_line
        )

        expect(checkbox).to_be_visible()
        expect(checkbox).to_be_checked()