from playwright.sync_api import expect


class ViewModifyRecordsPage:

    ITEM_NAME = "Alpha Series Laptop 13” i5"
    TASK_ITEM_LABEL = "Item Code : LT-ALP-13-I5Item"

    def __init__(self, page):
        self.page = page

    # =====================
    # Locators
    # =====================

    @property
    def control_panel_link(self):
        return self.page.get_by_role("link", name="Control Panel").first

    @property
    def view_modify_records_link(self):
        return self.page.get_by_role(
            "link",
            name="View / Modify Records"
        ).first

    @property
    def submit_continue_btn(self):
        return self.page.get_by_role(
            "button",
            name="Submit & Continue"
        )

    @property
    def edit_online_btn(self):
        return self.page.get_by_role(
            "button",
            name="Edit Online"
        )

    @property
    def exit_edit_mode_btn(self):
        return self.page.get_by_role(
            "button",
            name="Exit Edit Mode"
        )

    @property
    def save_btn(self):
        return self.page.get_by_text("Save")

    @property
    def configuration_input(self):
        return self.page.locator(
            "input[id='item_hierarchy_mapping__configuration']"
        )

    # =====================
    # Actions
    # =====================

    def open_view_modify_records(self):
        self.control_panel_link.click()
        self.view_modify_records_link.click()

        self.page.get_by_role("checkbox").nth(2).click()
        self.submit_continue_btn.click()

    def verify_invalid_request_error(self):
        toast = self.page.get_by_text(
            "Invalid request. Please check your input and try again."
        )

        toast.wait_for(state="visible", timeout=10000)

        assert toast.is_visible(), \
            "Error toast notification not displayed"

    def edit_item_description(self, description):

        self.page.wait_for_timeout(2000)

        self.edit_online_btn.click()

        self.page.wait_for_timeout(2000)

        self.page.get_by_text("Edit").nth(2).click()

        item_description = self.page.get_by_role(
            "cell",
            name=self.ITEM_NAME
        ).locator("#item_description")

        item_description.click()
        item_description.press("ControlOrMeta+a")
        item_description.fill(description)

        self.save_btn.click()

        self.exit_edit_mode_btn.click()

    def edit_configuration_code(self, config_code):

        table = self.page.locator(".ant-table-body")

        table.evaluate("""
        (el) => {
            el.scrollLeft = el.scrollWidth;
        }
        """)

        self.page.wait_for_timeout(2000)

        self.edit_online_btn.click()

        self.page.wait_for_timeout(2000)

        self.page.get_by_text("Edit").nth(2).click()

        self.configuration_input.click()
        self.configuration_input.press("ControlOrMeta+a")
        self.configuration_input.fill(config_code)

        self.save_btn.click()

    def verify_task_status(self, updated_description):

        self.page.get_by_role(
            "link",
            name="Task Status"
        ).click()

        self.page.get_by_role(
            "button",
            name="View"
        ).nth(2).click()

        self.page.locator(
            ".lucide.lucide-chevron-down"
        ).click()

        expect(
            self.page.get_by_label(self.TASK_ITEM_LABEL)
        ).to_contain_text(updated_description)