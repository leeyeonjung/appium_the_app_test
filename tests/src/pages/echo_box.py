# tests/src/pages/echo_box.py

# Standard library
import logging
from time import sleep

# Third-party libraries
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

# Local modules
from tests.src.locaters import echo_box_locaters as loc

log = logging.getLogger(__name__)


class EchoBoxPage:
    """Echo Box 화면의 기능 정의"""

    def __init__(self, driver):
        self.driver = driver

    def open_echo_box(self):
        """홈화면에서 Echo Box 클릭"""
        self.driver.find_element(By.XPATH, loc.ITEM_INDEX).click()
        log.debug("Echo Box 화면 진입")

    def get_title_text(self):
        """상단 Title 텍스트 반환"""
        title = self.driver.find_element(By.XPATH, loc.TITLE)
        log.debug(f"Title text: {title.text}")
        return title.text

    def get_placeholder_text(self):
        """입력창 placeholder 텍스트 반환"""
        input_field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, loc.INPUT_FIELD)
        log.debug(f"Placeholder text: {input_field.text}")
        return input_field.text

    def input_message(self, message: str):
        """입력창에 텍스트 입력"""
        input_field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, loc.INPUT_FIELD)
        input_field.send_keys(message)
        log.debug(f"입력 텍스트: {message}")

    def save_message(self):
        """Save 버튼 클릭"""
        save_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, loc.SAVE_BUTTON)
        save_button.click()
        sleep(0.5)
        log.debug("메시지 저장 완료")

    def get_saved_message(self):
        """저장된 메시지 반환"""
        result = self.driver.find_element(By.XPATH, loc.RESULT_TEXT)
        log.debug(f"저장된 메시지: {result.text}")
        return result.text