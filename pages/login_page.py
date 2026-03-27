
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "userEmail")
    PASSWORD_INPUT = (By.ID, "userPassword")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGO = (By.CSS_SELECTOR, ".company-logo")
    ERROR_MESSAGE = (By.XPATH, "//p[text()='Invalid credentials']")
    ERROR_MESSAGE1 = (By.XPATH, "//p[text()='*required'][1]")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-success, .alert-success")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".forgot-pswd")
    PAGE_HEADING = (By.CSS_SELECTOR, ".welcomeMessage")

    def navigate_to_login(self):
        self.open_url(self.config.get_base_url())
        self.wait_for_page_load()

    def enter_username(self, username: str):
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.log.info(f"Logging in with user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def login_with_valid_credentials(self):
        self.login(
            self.config.get_username(),
            self.config.get_password()
        )

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_element_displayed(self.ERROR_MESSAGE)
    def is_error_displayed1(self) -> bool:
        return self.is_element_displayed(self.ERROR_MESSAGE1)

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)

    def check_remember_me(self):
        if not self.is_element_selected(self.REMEMBER_ME_CHECKBOX):
            self.click(self.REMEMBER_ME_CHECKBOX)

    def get_all_input_field_count(self) -> int:
        return self.get_element_count(self.ALL_INPUT_FIELDS)

    def is_login_page_loaded(self) -> bool:
        return self.is_element_displayed(self.USERNAME_INPUT)

    def get_page_title(self) -> str:
        return self.get_title()
