# tests/src/locaters/login_screen_locaters.py
# Login Screen 주요 Locators

# 홈 화면 리스트에서 Login Screen
ITEM_INDEX = '(//android.view.ViewGroup[@resource-id="RNE__LISTITEM__padView"])[2]'

# Login Screen 화면 내에서의 title
TITLE = '//android.widget.LinearLayout[@resource-id="com.appiumpro.the_app:id/action_bar_root"]//android.widget.TextView'

# id,pw 입력 필드
USERNAME = 'username'
PASSWORD = 'password'

# Login Button
LOGIN_BTN = 'loginBtn'
# Logout Button
LOGOUT_BTN = 'Logout'

# TextView 텍스트 리스트 확인용 container
CONTAINER = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout'

# Alert Message
ALERT_MSG = 'android:id/message'