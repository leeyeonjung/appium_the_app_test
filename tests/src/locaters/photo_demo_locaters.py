# tests/src/locaters/photo_demo_locaters.py
# Photo Demo 주요 Locators

# 홈 화면 리스트에서 Photo Demo
MENU_ITEM = '(//android.view.ViewGroup[@resource-id="RNE__LISTITEM__padView"])[7]'

# Photo Demo 화면 내에서의 title
TITLE_TEXT = (
    '//android.widget.LinearLayout[@resource-id="com.appiumpro.the_app:id/action_bar_root"]'
    '//android.widget.TextView'
)

# Photo Demon 화면 내의 image 요소들
IMAGE_VIEWS = "//android.widget.ScrollView//android.widget.ImageView"

# 각 이미지의 안내 문구
DIALOG_TEXT = '//android.widget.TextView[@resource-id="android:id/message"]'

# Ok button
BUTTON_OK = '//android.widget.Button[@resource-id="android:id/button1"]'
