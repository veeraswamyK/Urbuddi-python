import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions, Options
from config.config_reader import ConfigReader
from pages.login_page import LoginPage
from utilities.screenshot import take_screenshot
import pytest

@pytest.fixture
def driver():
    config = ConfigReader()
    browser = config.get_browser()


    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2})
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--disable-notifications")
        options.set_preference("dom.webnotifications.enabled", False)
        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options=ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2})
        driver = webdriver.Edge(options=options)

    else:
        raise Exception(f" Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()
# def get_browser_list():
#     return ConfigReader().get_browsers()

# @pytest.fixture(params=ConfigReader().config.get("browsers", ["chrome"]))
#
# def driver(request):
#     browser = request.param
#     config = ConfigReader()
#
#     if browser == "chrome":
#         driver = webdriver.Chrome()
#
#     elif browser == "firefox":
#         driver = webdriver.Firefox()
#
#     elif browser == "edge":
#         driver = webdriver.Edge()
#
#     else:
#         raise Exception(f"Unsupported browser: {browser}")
#
#     yield driver
#     driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)
@pytest.fixture
def config():
    return ConfigReader()
def pytest_runtest_setup(item):
    print(f"\n[HOOK] Setup → {item.name}")

def pytest_runtest_call(item):
    print(f"[HOOK] Call → {item.name}")



def pytest_runtest_teardown(item):
    driver = item.funcargs.get("driver", None)

    if driver is not None:
        if hasattr(item, "rep_call") and item.rep_call.failed:
            path = take_screenshot(driver, item.name)
            print(f"\n📸 Screenshot saved at: {path}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )