# src/locaters/webview_demo_locaters.py
# Webview Demo 주요 Locators

# 홈 화면 리스트에서 Webview Demo 항목
MENU_ITEM = '(//android.view.ViewGroup[@resource-id="RNE__LISTITEM__padView"])[4]'

# Native 영역
INPUT_FIELD = "urlInput"
GO_BUTTON = "navigateBtn"

# WebView 내부 공통 요소
HAMBURGER_ICON = '/html/body/div/div/div[2]/div/div/a/img'
TITLE_TEXT = '/html/body/div/div/div[3]/h1'

# 메뉴 항목 공통 템플릿
MENU_TEMPLATE = '/html/body/div/div/div[2]/div/ul/li[{index}]/a'

# 메뉴 이름별 index 매핑
MENU_INDEX = {
    "GET_CERTIFIED": 1,
    "SUBSCRIBE": 2,
    "LATEST": 3,
    "ALL_EDITIONS": 4,
    "SPONSORS": 5,
    "CONTACT": 6,
    "ABOUT": 7,
}
