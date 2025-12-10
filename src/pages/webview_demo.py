# src/pages/webview_demo.py

# Standard library
import logging

# Third-party libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

# Local modules
from src.locaters import webview_demo_locaters as loc

log = logging.getLogger(__name__)


class WebviewDemoPage:
    """Webview Demo 화면의 기능 정의"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def open_webview_demo(self):
        """홈 화면에서 Webview Demo 클릭"""
        log.debug("Webview Demo 화면 진입")
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, loc.MENU_ITEM)))
        element.click()


    def get_placeholder_text(self):
        """입력창 placeholder 텍스트 반환"""
        field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, loc.INPUT_FIELD)))
        log.debug(f"Placeholder text: {field.text}")
        return field.text


    def input_url(self, url: str):
        """URL 입력"""
        log.debug(f"URL 입력: {url}")
        field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, loc.INPUT_FIELD)))
        field.send_keys(url)


    def click_go_button(self):
        """Go 버튼 클릭"""
        log.debug("Go 버튼 클릭")
        element = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, loc.GO_BUTTON)))
        element.click()


    def switch_to_webview(self):
        """Context를 WebView로 전환"""
        log.debug("Context를 WebView로 전환")
        self.driver.switch_to.context("WEBVIEW_com.appiumpro.the_app")


    def click_hamburger(self):
        """햄버거 메뉴 클릭"""
        log.debug("햄버거 메뉴 클릭")
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, loc.HAMBURGER_ICON)))
        element.click()


    def click_menu_by_name(self, name: str):
        """메뉴 이름으로 클릭"""
        key = name.upper()
        index = loc.MENU_INDEX.get(key)
        if not index:
            raise ValueError(f"존재하지 않는 메뉴 이름: {name}")
        xpath = loc.MENU_TEMPLATE.format(index=index)
        log.debug(f"메뉴 클릭: {name} (li[{index}])")
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()


    def get_title_text(self):
        """페이지 타이틀 텍스트 반환"""
        log.debug("페이지 타이틀 텍스트 반환")
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, loc.TITLE_TEXT)))
        return element.text
