import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.config_reader import ConfigReader
from pages.login_page import LoginPage
from utilities.screenshot import take_screenshot


@pytest.fixture
def driver():
    config = ConfigReader()
    browser = config.get_browser()

    if browser == "chrome":
        options = ChromeOptions()

        if config.is_headless():
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-notifications")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()

        if config.is_headless():
            options.add_argument("--headless")

        options.set_preference("dom.webnotifications.enabled", False)

        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = ChromeOptions()

        if config.is_headless():
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-notifications")

        driver = webdriver.Edge(options=options)

    else:
        raise Exception(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()

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
            print(f"\nScreenshot saved at: {path}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep
        if rep.failed:
            driver = item.funcargs.get("driver")
            if driver:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )