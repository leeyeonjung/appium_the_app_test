# tests/src/pages/webview_demo.py

# Standard library
import logging

# Third-party libraries
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

# Local modules
from tests.src.locaters import webview_demo_locaters as loc

log = logging.getLogger(__name__)


class WebviewDemoPage:
    """Webview Demo 화면의 기능 정의"""

    def __init__(self, driver):
        self.driver = driver

    def open_webview_demo(self):
        """홈 화면에서 Webview Demo 클릭"""
        log.debug("Webview Demo 화면 진입")
        self.driver.find_element(By.XPATH, loc.MENU_ITEM).click()

    def get_placeholder_text(self):
        """입력창 placeholder 텍스트 반환"""
        field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, loc.INPUT_FIELD)
        log.debug(f"Placeholder text: {field.text}")
        return field.text

    def input_url(self, url: str):
        """URL 입력"""
        log.debug(f"URL 입력: {url}")
        field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, loc.INPUT_FIELD)
        field.send_keys(url)

    def click_go_button(self):
        """Go 버튼 클릭"""
        log.debug("Go 버튼 클릭")
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, loc.GO_BUTTON).click()

    def switch_to_webview(self):
        """Context를 WebView로 전환"""
        log.debug("Context를 WebView로 전환")
        self.driver.switch_to.context("WEBVIEW_com.appiumpro.the_app")

    def click_hamburger(self):
        """햄버거 메뉴 클릭"""
        log.debug("햄버거 메뉴 클릭")
        self.driver.find_element(By.XPATH, loc.HAMBURGER_ICON).click()

    def click_menu_by_name(self, name: str):
        """메뉴 이름으로 클릭"""
        key = name.upper()
        index = loc.MENU_INDEX.get(key)
        if not index:
            raise ValueError(f"존재하지 않는 메뉴 이름: {name}")
        xpath = loc.MENU_TEMPLATE.format(index=index)
        log.debug(f"메뉴 클릭: {name} (li[{index}])")
        self.driver.find_element(By.XPATH, xpath).click()

    def get_title_text(self):
        """페이지 타이틀 텍스트 반환"""
        log.debug("페이지 타이틀 텍스트 반환")
        return self.driver.find_element(By.XPATH, loc.TITLE_TEXT).text