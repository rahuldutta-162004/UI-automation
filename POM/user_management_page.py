from playwright.sync_api import expect


class UserManagementPage:

    def __init__(self, page):
        self.page = page

    #locators

    @property
    def user_management_link(self):
        return self.page.get_by_role(
            "link",
            name="User Management"
        ).first

    @property
    def add_user_btn(self):
        return self.page.get_by_role(
            "button",
            name="Add User"
        )

    @property
    def first_name_txt(self):
        return self.page.get_by_role(
            "textbox",
            name="Enter first name"
        )

    @property
    def last_name_txt(self):
        return self.page.get_by_role(
            "textbox",
            name="Enter last name"
        )

    @property
    def mobile_txt(self):
        return self.page.get_by_role(
            "textbox",
            name="Country code + number (e.g.,"
        )

    @property
    def email_txt(self):
        return self.page.get_by_role(
            "textbox",
            name="Email ID *"
        )

    @property
    def domain_dropdown(self):
        return self.page.get_by_role(
            "combobox"
        ).filter(
            has_text="Select Domain"
        )

    @property
    def department_dropdown(self):
        return self.page.get_by_role(
            "combobox"
        ).filter(
            has_text="Select department"
        )

    @property
    def save_next_btn(self):
        return self.page.get_by_role(
            "button",
            name="Save & Next"
        )

    @property
    def add_selected_btn(self):
        return self.page.get_by_role(
            "button",
            name="Add Selected"
        )

    @property
    def save_user_btn(self):
        return self.page.get_by_role(
            "button",
            name="Save User"
        )

    @property
    def confirm_create_user_btn(self):
        return self.page.get_by_role(
            "button",
            name="Confirm & Create User"
        )

    #actions

    def open_user_management(self):
        self.user_management_link.click()

    def click_add_user(self):
        self.add_user_btn.click()

    def fill_user_details(
        self,
        first_name,
        last_name,
        mobile,
        email
    ):
        self.first_name_txt.fill(first_name)
        self.last_name_txt.fill(last_name)
        self.mobile_txt.fill(mobile)
        self.email_txt.fill(email)

    def select_domain(self, domain="gmail.com"):
        self.domain_dropdown.click()

        self.page.get_by_label(
            domain
        ).get_by_text(
            domain
        ).click()

    def select_department(
        self,
        department="Distribution"
    ):
        self.department_dropdown.click()

        self.page.get_by_role(
            "option",
            name=department
        ).click()

    def save_and_next(self):
        self.save_next_btn.click()
        self.page.wait_for_load_state("networkidle")

    def add_role(self, role_name):

        role = self.page.locator(
            "span.text-sm.flex-1",
            has_text=role_name
        )

        role.wait_for()
        role.click()

        self.add_selected_btn.click()

    def save_user(self):

        self.save_user_btn.click()

        self.confirm_create_user_btn.click()

        self.page.wait_for_timeout(3000)

    def create_user(
        self,
        first_name,
        last_name,
        mobile,
        email
    ):

        self.open_user_management()

        self.click_add_user()

        self.fill_user_details(
            first_name,
            last_name,
            mobile,
            email
        )

        self.select_domain()

        self.select_department()

        self.save_and_next()

        self.add_role("Sales")

        self.add_role("Finished Good")

        self.add_role("Plant")

        self.save_user()

    def verify_failed_user_creation(self):

        toast = self.page.get_by_text(
            "Failed to create user"
        )

        toast.wait_for(
            state="visible",
            timeout=10000
        )

        assert toast.is_visible()

    def search_user(self, email):

        self.page.locator(
            "#email > .flex > .flex-1 > "
            ".ant-table-filter-column > "
            ".ant-dropdown-trigger > "
            ".anticon > svg"
        ).click()

        self.page.get_by_role(
            "textbox",
            name="Search"
        ).fill(email)

        self.page.get_by_text(
            email,
            exact=True
        ).click()

        apply_filter = self.page.get_by_role(
            "button",
            name="Apply Filter"
        )

        if (
            apply_filter.count() > 0
            and apply_filter.is_visible()
            and apply_filter.is_enabled()
        ):
            apply_filter.click()

    def verify_user_exists(self, email):

        self.page.locator(
            f"text={email}"
        ).wait_for(timeout=15000)

        table_text = self.page.locator(
            "tbody"
        ).text_content()

        assert email in table_text