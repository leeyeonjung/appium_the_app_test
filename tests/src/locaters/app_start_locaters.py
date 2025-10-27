# tests/src/locaters/app_start_locaters.py
# app start 주요 Locators

# 리스트 아이템 공통 템플릿 (index 위치를 포맷으로 지정)
ITEM_TEMPLATE = '(//android.view.ViewGroup[@resource-id="RNE__LISTITEM__padView"])[{index}]'

# 각 아이템 Title / Description
ITEM_TITLE = '//android.widget.TextView[@resource-id="listItemTitle"]'

# 세션 확인용 Appium WebDriver 문자열
SESSION_CHECK = "appium.webdriver.webdriver.WebDriver"