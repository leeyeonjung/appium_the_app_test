# tests/src/pages/app_start.py

# Standard library
import logging

# Third-party libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local modules
from tests.src.locaters import app_start_locaters as loc

log = logging.getLogger(__name__)


class HomePage:
    """홈 화면 항목 정보 조회 및 클릭 기능"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def is_driver_active(self) -> bool:
        """Appium 세션이 정상 연결되었는지 확인"""
        return loc.SESSION_CHECK in str(self.driver)


    def get_item_elements(self, index: int):
        """index 번째 리스트 항목 내 TextView 요소 2개 반환"""
        xpath = f'{loc.ITEM_TEMPLATE.format(index=index)}{loc.ITEM_TITLE}'
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = self.driver.find_elements(By.XPATH, xpath)
        log.debug(f"[INDEX {index}] Found {len(elements)} TextView elements")
        return elements


    def get_item_texts(self, index: int):
        """index 번째 항목의 Title / Description 텍스트 반환"""
        elements = self.get_item_elements(index)
        title_text = elements[0].text if elements else None
        desc_text = elements[1].text if len(elements) > 1 else None
        log.debug(f"[READ] index={index} title='{title_text}', desc='{desc_text}'")
        return title_text, desc_text
