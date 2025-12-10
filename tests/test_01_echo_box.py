# tests/test_01_echo_box.py

# Third-party libraries
import pytest_check as check

# Local modules
from src.actions.echo_box import EchoBoxPage


def test_into_echo_box(wd):
    """Echo Box 화면 진입 확인"""
    page = EchoBoxPage(wd)
    page.open_echo_box()
    title = page.get_title_text()
    check.equal(title, "Echo Screen")


def test_echo_box_placeholder(wd):
    """Echo Box 입력창의 placeholder 문구가 “Say something”인지 확인"""
    page = EchoBoxPage(wd)
    page.open_echo_box()
    placeholder = page.get_placeholder_text()
    check.equal(placeholder, "Say something")


def test_inputfield_function_01(wd):
    """입력한 텍스트가 저장 후 동일하게 표시되는지 확인"""
    page = EchoBoxPage(wd)
    page.open_echo_box()

    input_text = "Hello Test1"
    page.input_message(input_text)
    page.save_message()

    saved_text = page.get_saved_message()
    check.equal(saved_text, input_text)


def test_inputfield_function_02(wd):
    """새 텍스트 입력 시 이전 데이터가 덮어쓰기 되어 최신 메시지만 표시되는지 확인"""
    page = EchoBoxPage(wd)
    page.open_echo_box()

    input_text1 = "Hello Test1"
    input_text2 = "Hello Test2"

    page.input_message(input_text1)
    page.save_message()

    page.input_message(input_text2)
    page.save_message()

    saved_text = page.get_saved_message()
    check.equal(saved_text, input_text2)
