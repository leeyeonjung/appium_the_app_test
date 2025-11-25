# tests/src/pages/login_screen.py

# Standard library
import logging
from time import sleep

# Third-party libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

# Local modules
from tests.src.locaters import login_screen_locaters as loc

log = logging.getLogger(__name__)


class LoginScreenPage:
    """Login Screen 화면의 기능 정의"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def open_login_screen(self):
        """홈 화면에서 Login Screen 클릭"""
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, loc.ITEM_INDEX)))
        element.click()
        log.debug("Login Screen 화면 진입")


    def get_title_text(self):
        """상단 타이틀 텍스트 반환"""
        el = self.wait.until(EC.presence_of_element_located((By.XPATH, loc.TITLE)))
        return el.text


    def get_placeholder_texts(self):
        """ID, PW 입력창 placeholder 반환"""
        id_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, loc.USERNAME)))
        pw_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, loc.PASSWORD)))
        return id_field.text, pw_field.text


    def input_credentials(self, username: str, password: str):
        """아이디/비밀번호 입력"""
        id_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, loc.USERNAME)))
        pw_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, loc.PASSWORD)))
        id_field.send_keys(username)
        pw_field.send_keys(password)
        log.debug(f"입력: id={username}, pw={password}")


    def click_login(self):
        """로그인 버튼 클릭"""
        btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, loc.LOGIN_BTN)))
        btn.click()
        sleep(1.0)
        log.debug("로그인 버튼 클릭 완료")


    def click_logout(self):
        """로그아웃 버튼 클릭"""
        btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, loc.LOGOUT_BTN)))
        btn.click()
        sleep(1.0)
        log.debug("로그아웃 완료")


    def get_alert_message(self):
        """로그인 실패 시 Alert 메시지 반환"""
        el = self.wait.until(EC.presence_of_element_located((By.ID, loc.ALERT_MSG)))
        return el.text


    def get_login_result_texts(self):
        """로그인 성공 후 Secret Area 화면의 TextView 텍스트 리스트 반환"""
        container = self.wait.until(EC.presence_of_element_located((By.XPATH, loc.CONTAINER)))
        texts = [el.text for el in container.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")]
        log.debug(f"화면 텍스트: {texts}")
        return texts