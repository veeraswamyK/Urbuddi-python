import allure
import pytest
from config.config_reader import ConfigReader
from conftest import login_page
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

class TestLogin:
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.login
    @allure.feature("Login Feature")
    @allure.story("Valid Login")
    @allure.title("TC_001:User able to login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_user(self, driver, login_page, config):
        with allure.step("open url"):
            login_page.navigate_to_login()
        with allure.step("Enter valid user-name"):
            login_page.enter_username(config.get_username())
        with allure.step("Enter valid password"):
            login_page.enter_password(config.get_password())
        login_page.click_login()
        dashboard = DashboardPage(driver)
        assert dashboard.is_dashboard_loaded()

    @pytest.mark.smoke
    @pytest.mark.login
    @allure.feature("Login Feature")
    @allure.story("Valid Login")
    @allure.title("TC_002:User unable to login with invalid email")
    def test_invalid_username(self, driver, login_page, config):
        login_page.navigate_to_login()
        login_page.login("wrong@email.com", config.get_password())
        assert login_page.is_error_displayed()
    @allure.feature("Login Feature")
    @allure.story("Valid Login")
    @allure.title("TC_003:User unable to login without credentials")
    @pytest.mark.login
    def test_empty_credentials(self, driver, login_page):
        login_page.navigate_to_login()
        login_page.click_login()  # click without entering anything
        assert login_page.is_error_displayed1()
    @allure.feature("Login Feature")
    @allure.story("Valid Login")
    @allure.title("TC_001:User unable to login with invalid password")
    @pytest.mark.login
    def test_wrong_password(self, driver, login_page, config):
        login_page.navigate_to_login()
        login_page.login(config.get_username(), "WrongPassword@123")
        assert login_page.is_error_displayed()

    @pytest.mark.smoke
    @pytest.mark.login
    def test_invalid_password(self, driver, login_page, config):
        login_page.navigate_to_login()
        login_page.login(config.get_username(),"wrong@email.com")
        assert login_page.is_error_displayed()

    @pytest.mark.smoke
    @pytest.mark.multipleuser
    @allure.feature("Login Feature")
    @allure.story("Valid Login")
    def test_with_multiple_users(self, login_page):
        login_page.navigate_to_login()

    @pytest.mark.smoke
    def test_one(self):
        print("Executing test_one")
    assert True

    @pytest.mark.smoke
    def test_two(self):
        print("Executing test_two")
    assert True