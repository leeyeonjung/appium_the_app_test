# tests/test_02_login_screen.py

# Third-party libraries
import pytest_check as check

# Local modules
from src.pages.login_screen import LoginScreenPage


def test_into_login_screen(wd):
    """Login Screen 화면 진입 확인"""
    page = LoginScreenPage(wd)
    page.open_login_screen()
    title = page.get_title_text()
    check.equal(title, "Login")


def test_login_screen_placeholder(wd):
    """ID 및 Password 입력란의 placeholder 문구 표기 확인"""
    page = LoginScreenPage(wd)
    page.open_login_screen()
    id_text, pw_text = page.get_placeholder_texts()
    check.equal(id_text, "Username")
    check.equal(pw_text, "Password")


def test_login_success(wd):
    """유효한 계정 정보 입력 시 로그인 성공 하는지 확인"""
    page = LoginScreenPage(wd)
    page.open_login_screen()
    page.input_credentials("alice", "mypassword")
    page.click_login()

    result_texts = page.get_login_result_texts()
    check.equal("Secret Area" in result_texts, True)
    check.equal("You are logged in as alice" in result_texts, True)


def test_login_fail(wd):
    """비유효 계정 정보 입력 시 로그인 실패하여 경고 메시지가 정상 출력되는지 확인"""
    page = LoginScreenPage(wd)
    page.open_login_screen()
    page.input_credentials("alice", "test")
    page.click_login()
    alert_msg = page.get_alert_message()
    check.equal(alert_msg, "Invalid login credentials, please try again")


def test_logout_success(wd):
    """로그인 후 로그아웃 시 다시 Login 화면으로 돌아오는지 확인"""
    page = LoginScreenPage(wd)
    page.open_login_screen()
    page.input_credentials("alice", "mypassword")
    page.click_login()
    page.click_logout()
    title = page.get_title_text()
    check.equal(title, "Login")
