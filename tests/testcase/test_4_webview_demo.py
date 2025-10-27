# tests/testcase/test_4_webview_demo.py
# Standard library
from time import sleep

# Third-party libraries
import pytest_check as check

# Local modules
from tests.src.pages.webview_demo import WebviewDemoPage


def test_webview_demo_placeholder(wd):
    """Webview Demo 입력창 placeholder 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    placeholder = page.get_placeholder_text()
    check.equal(placeholder, "https://appiumpro.com")


def test_webview_context(wd):
    """Webview 전환 후 context 이름 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    check.equal(wd.current_context, "WEBVIEW_com.appiumpro.the_app")


def test_get_certified(wd):
    """‘Get Certified’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("get_certified")
    title = page.get_title_text()
    check.equal(title, 'Appium Pro Training, Tutorials, and Certification')


def test_subscribe(wd):
    """‘Subscribe’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("subscribe")
    title = page.get_title_text()
    check.equal(title, 'Subscribe Now')


def test_latest(wd):
    """‘Latest’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("latest")
    sleep(1)
    title = page.get_title_text()
    check.equal(title, 'Edition 124')


def test_all_editions(wd):
    """‘All Editions’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("all_editions")
    title = page.get_title_text()
    check.equal(title, 'All Editions')


def test_sponsors(wd):
    """‘Sponsors’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("sponsors")
    title = page.get_title_text()
    check.equal(title, 'Sponsors')


def test_contact(wd):
    """‘Contact’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("contact")
    title = page.get_title_text()
    check.equal(title, 'Contact Us')


def test_about(wd):
    """‘About’ 메뉴 진입 및 타이틀 확인"""
    page = WebviewDemoPage(wd)
    page.open_webview_demo()
    page.input_url("https://appiumpro.com")
    page.click_go_button()
    page.switch_to_webview()
    page.click_hamburger()
    page.click_menu_by_name("about")
    title = page.get_title_text()
    check.equal(title, 'About')