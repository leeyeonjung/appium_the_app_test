# tests/src/pages/photo_demo.py

# Standard library
import logging
from time import sleep
from pathlib import Path

# Third-party libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH

# Local modules
import tests.src.locaters.photo_demo_locaters as loc

log = logging.getLogger(__name__)


class PhotoDemoPage:
    """Photo Demo 화면의 기능 정의"""

    def __init__(self, driver):
        self.driver = driver
        self.base_dir = Path(__file__).resolve().parents[2]  # tests/
        self.image_dir = self.base_dir / "image"

    def open_photo_demo(self):
        """홈 화면에서 photo demo 클릭"""
        log.debug("Photo Demo 화면 진입")
        self.driver.find_element(By.XPATH, loc.MENU_ITEM).click()

    def get_title_text(self):
        """화면 title text 반환"""
        return self.driver.find_element(By.XPATH, loc.TITLE_TEXT).text

    def get_window_size(self):
        """스크롤을 위한 기기 화면 사이즈 반환"""
        return self.driver.get_window_rect()

    def swipe_up(self, step: float = 0.25, duration: int = 15000):
        """
        화면을 위로 스와이프 (Selenium 4 W3C ActionBuilder)
        :param step: 이동 거리 비율 (0.25 → 화면 높이의 25%)
        :param duration: 제스처 시간(ms) (너무 짧으면 플링으로 인식될 수 있음)
        """
        win = self.get_window_size()
        start_x = win["width"] // 2
        start_y = int(win["height"] * 0.75)
        end_y   = int(win["height"] * (0.75 - step))

        log.debug(f"[SWIPE_UP] ({start_x},{start_y}) → ({start_x},{end_y}), step={step}, duration={duration}ms")

        # 터치 포인터 장치 정의
        finger = PointerInput(POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger)

        # 제스처 구성
        pa = actions.pointer_action
        pa.move_to_location(start_x, start_y)
        pa.pointer_down()
        # duration은 초 단위로 pause
        pa.pause(duration / 1000.0)
        pa.move_to_location(start_x, end_y)
        pa.release()

        actions.perform()
        sleep(1.2)

    def get_all_image_views(self):
        """화면 내 전체 image list 반환"""
        return self.driver.find_elements(By.XPATH, loc.IMAGE_VIEWS)

    def tap_element(self, el):
        """이미지 클릭"""
        el.click()
        sleep(0.5)

    def get_dialog_text(self):
        return self.driver.find_element(By.XPATH, loc.DIALOG_TEXT).text.strip()

    def close_dialog_ok(self):
        """이미지 화면 ok 버튼 클릭"""
        self.driver.find_element(By.XPATH, loc.BUTTON_OK).click()
        sleep(0.8)

    def capture_visible_square_images(self, save_dir, seen_rects: set, captured: set, use_scroll_view=True):
        """현재 화면의 보이는 정사각형 이미지들을 파일로 저장 (중복 방지 로직 적용)"""
        win = self.get_window_size()
        win_w, win_h = win["width"], win["height"]

        elements = self.get_all_image_views() if use_scroll_view else self.get_all_image_views()
        log.debug(f"[SCAN] Found {len(elements)} ImageViews")

        for el in elements:
            r = el.rect
            x, y, w, h = r["x"], r["y"], r["width"], r["height"]
            bottom, right = y + h, x + w

            fully_visible = (x >= -10 and y >= 0 and right <= win_w + 10 and bottom <= win_h + 30)
            square_like   = abs(w - h) < 20
            if not (fully_visible and square_like):
                continue

            # 중복 판별(오차 허용)
            duplicate = False
            for (sx, sy, sw, sh) in seen_rects:
                if abs(sx - x) < 25 and abs(sy - y) < 25 and abs(sw - w) < 10 and abs(sh - h) < 10:
                    duplicate = True
                    break
            if duplicate:
                continue

            path = save_dir / f"captured_{len(captured)+1}.png"
            with open(path, "wb") as f:
                f.write(el.screenshot_as_png)
            seen_rects.add((x, y, w, h))
            captured.add(str(path))
            log.debug(f"[SAVE] {path.name} ({w}x{h}) at (x={x}, y={y})")