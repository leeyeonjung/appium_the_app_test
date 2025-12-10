# tests/test_00_app_start.py

# Third-party libraries
import pytest_check as check

# Local modules
from src.actions.app_start import HomePage


def test_setup(wd):
    """앱 실행 상태 확인"""
    page = HomePage(wd)
    check.equal(page.is_driver_active(), True, "Appium driver is not active")


def test_homescreen_01(wd):
    """홈 화면의 Echo Box 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Echo Box"
    expected_desc = "Write something and save to local memory"
    title, desc = page.get_item_texts(1)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_02(wd):
    """홈 화면의 Login Screen 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Login Screen"
    expected_desc = "A fake login screen for testing"
    title, desc = page.get_item_texts(2)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_03(wd):
    """홈 화면의 Clipboard Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Clipboard Demo"
    expected_desc = "Mess around with the clipboard"
    title, desc = page.get_item_texts(3)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_04(wd):
    """홈 화면의 Webview Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Webview Demo"
    expected_desc = "Explore the possibilities of hybrid apps"
    title, desc = page.get_item_texts(4)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_05(wd):
    """홈 화면의 Dual Webview Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Dual Webview Demo"
    expected_desc = "Automate apps with multiple webviews"
    title, desc = page.get_item_texts(5)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_06(wd):
    """홈 화면의 List Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "List Demo"
    expected_desc = "Scroll through a list of stuff"
    title, desc = page.get_item_texts(6)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_07(wd):
    """홈 화면의 Photo Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Photo Demo"
    expected_desc = "Some photos with no distinguishing IDs"
    title, desc = page.get_item_texts(7)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_08(wd):
    """홈 화면의 Geolocation Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Geolocation Demo"
    expected_desc = "See your current location"
    title, desc = page.get_item_texts(8)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_09(wd):
    """홈 화면의 Picker Demo 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Picker Demo"
    expected_desc = "Use some picker wheels for fun and profit"
    title, desc = page.get_item_texts(9)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)


def test_homescreen_10(wd):
    """홈 화면의 Verify Phone Number 메뉴 타이틀 및 설명 문구 확인"""
    page = HomePage(wd)
    expected_title = "Verify Phone Number"
    expected_desc = "A fake SMS auto-verification screen"
    title, desc = page.get_item_texts(10)
    check.equal(title, expected_title)
    check.equal(desc, expected_desc)
