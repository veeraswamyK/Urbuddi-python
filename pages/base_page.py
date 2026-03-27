
import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    StaleElementReferenceException, ElementNotInteractableException
)
from config.config_reader import ConfigReader
from utilities.logger import Logger


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigReader()
        self.wait = WebDriverWait(driver, self.config.get_explicit_wait())
        self.log = Logger.get_logger(self.__class__.__name__)
        self.actions = ActionChains(driver)


    def open_url(self, url: str):
        self.log.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def go_back(self):
        self.driver.back()

    def refresh(self):
        self.driver.refresh()


    def wait_for_element_visible(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_present(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_text_in_element(self, locator: tuple, text: str):
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_element_invisible(self, locator: tuple):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_url_contains(self, url_fragment: str):
        return self.wait.until(EC.url_contains(url_fragment))


    def fluent_wait(self, locator: tuple, timeout: int = 30, poll: float = 0.5):
        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=poll,
            ignored_exceptions=[StaleElementReferenceException, NoSuchElementException]
        )
        return wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple):
        element = self.wait_for_element_clickable(locator)
        self.log.info(f"Clicking: {locator}")
        element.click()

    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        element = self.wait_for_element_visible(locator)
        if clear_first:
            element.clear()
        self.log.info(f"Typing '{text}' into {locator}")
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        element = self.wait_for_element_visible(locator)
        return element.text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        element = self.wait_for_element_present(locator)
        return element.get_attribute(attribute)

    def is_element_displayed(self, locator: tuple) -> bool:
        try:
            return self.wait_for_element_visible(locator).is_displayed()
        except TimeoutException:
            return False

    def is_element_enabled(self, locator: tuple) -> bool:
        try:
            element = self.wait_for_element_present(locator)
            return element.is_enabled()
        except TimeoutException:
            return False

    def is_element_selected(self, locator: tuple) -> bool:
        element = self.wait_for_element_present(locator)
        return element.is_selected()

    def press_enter(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        element.send_keys(Keys.ENTER)

    def press_tab(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        element.send_keys(Keys.TAB)

    def clear_with_ctrl_a(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    def select_by_visible_text(self, locator: tuple, text: str):
        element = self.wait_for_element_present(locator)
        Select(element).select_by_visible_text(text)

    def select_by_value(self, locator: tuple, value: str):
        element = self.wait_for_element_present(locator)
        Select(element).select_by_value(value)

    def select_by_index(self, locator: tuple, index: int):
        element = self.wait_for_element_present(locator)
        Select(element).select_by_index(index)

    def get_selected_option(self, locator: tuple) -> str:
        element = self.wait_for_element_present(locator)
        return Select(element).first_selected_option.text

    def get_all_dropdown_options(self, locator: tuple) -> list:
        element = self.wait_for_element_present(locator)
        return [opt.text for opt in Select(element).options]

    def hover_over_element(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def right_click(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        ActionChains(self.driver).context_click(element).perform()

    def double_click(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        ActionChains(self.driver).double_click(element).perform()

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple):
        source = self.wait_for_element_visible(source_locator)
        target = self.wait_for_element_visible(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def click_and_hold(self, locator: tuple):
        element = self.wait_for_element_visible(locator)
        ActionChains(self.driver).click_and_hold(element).perform()

    def js_click(self, locator: tuple):
        element = self.wait_for_element_present(locator)
        self.driver.execute_script("arguments[0].click();", element)
        self.log.info(f"JS clicked: {locator}")

    def js_scroll_into_view(self, locator: tuple):
        element = self.wait_for_element_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def js_scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def js_scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def js_set_value(self, locator: tuple, value: str):
        element = self.wait_for_element_present(locator)
        self.driver.execute_script(f"arguments[0].value='{value}';", element)

    def js_get_text(self, locator: tuple) -> str:
        element = self.wait_for_element_present(locator)
        return self.driver.execute_script("return arguments[0].innerText;", element)

    def js_highlight_element(self, locator: tuple):
        element = self.wait_for_element_present(locator)
        self.driver.execute_script(
            "arguments[0].style.border='3px solid yellow'", element
        )

    def accept_alert(self):
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.log.info(f"Accepting alert: {alert.text}")
        alert.accept()

    def dismiss_alert(self):
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def get_alert_text(self) -> str:
        self.wait.until(EC.alert_is_present())
        return self.driver.switch_to.alert.text

    def send_keys_to_alert(self, text: str):
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.send_keys(text)
        alert.accept()

    def switch_to_frame_by_locator(self, locator: tuple):
        frame = self.wait_for_element_present(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_frame_by_index(self, index: int):
        self.driver.switch_to.frame(index)

    def switch_to_frame_by_name(self, name: str):
        self.driver.switch_to.frame(name)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        self.driver.switch_to.parent_frame()

    def get_current_window_handle(self) -> str:
        return self.driver.current_window_handle

    def get_all_window_handles(self) -> list:
        return self.driver.window_handles

    def switch_to_new_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def switch_to_window_by_index(self, index: int):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    def close_current_window_and_switch_back(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_new_tab(self):
        self.driver.execute_script("window.open('');")
        self.switch_to_new_window()

    def take_screenshot(self, name: str = None) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        self.log.info(f"Screenshot saved: {filepath}")
        return filepath

    def take_element_screenshot(self, locator: tuple, name: str = None) -> str:
        element = self.wait_for_element_visible(locator)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"element_{name}_{timestamp}.png"
        screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)
        filepath = os.path.join(screenshots_dir, filename)
        element.screenshot(filepath)
        return filepath

    def scroll_to_element(self, locator: tuple):
        element = self.wait_for_element_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.3)

    def get_all_elements(self, locator: tuple) -> list:
        self.wait_for_element_present(locator)
        return self.driver.find_elements(*locator)

    def get_element_count(self, locator: tuple) -> int:
        elements = self.driver.find_elements(*locator)
        return len(elements)

    def wait_for_page_load(self, timeout: int = 30):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
