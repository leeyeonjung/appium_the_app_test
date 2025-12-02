# tests/src/locaters/echo_box_locators.py
# Echo Box 주요 Locators

# 홈 화면 리스트에서 Echo Box
ITEM_INDEX = '(//android.view.ViewGroup[@resource-id="RNE__LISTITEM__padView"])[1]'

# echo box 화면 내에서의 title
TITLE = (
    '//android.widget.LinearLayout[@resource-id="com.appiumpro.the_app:id/action_bar_root"]'
    '//android.widget.TextView'
)

# message input field
INPUT_FIELD = 'messageInput'

# 저장 Button
SAVE_BUTTON = 'messageSaveBtn'

# 저장 메세지
RESULT_TEXT = "//*[@resource-id='savedMessage']"
