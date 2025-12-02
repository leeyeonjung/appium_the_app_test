# tests/testcase/test_7_photo_demo.py
# Standard library
import logging
import os
from pathlib import Path
from time import sleep

# Third-party libraries
import pytest_check as check

# Local modules
from tests.src.pages.photo_demo import PhotoDemoPage
from tests.src.common_util import control_image as control_image

log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = BASE_DIR / "image"


def test_into_photo_demo(wd):
    """Photo Demo 화면 진입 확인"""
    page = PhotoDemoPage(wd)

    page.open_photo_demo()
    title = page.get_title_text()

    check.equal(title, "Photo Library. Tap a photo!")


def test_photo(wd):
    """표시된 이미지가 원본 이미지와 동일한지 확인"""
    page = PhotoDemoPage(wd)

    raw_device_id = wd.capabilities.get("udid") or wd.capabilities.get("deviceUDID") or "unknown_device"
    device_id = str(raw_device_id).replace(":", "_").replace("/", "_").replace("\\", "_")

    save_dir = BASE_DIR / "Result" / "image" / device_id / "test_photo"
    save_dir.mkdir(parents=True, exist_ok=True)

    page.open_photo_demo()
    sleep(1)

    expected = {
        str(IMAGE_DIR / "original_1.png"),
        str(IMAGE_DIR / "original_2.png"),
        str(IMAGE_DIR / "original_3.png"),
        str(IMAGE_DIR / "original_4.png"),
        str(IMAGE_DIR / "original_5.png"),
        str(IMAGE_DIR / "original_6.png"),
    }

    captured, seen_rects, verified_images = set(), set(), set()

    # 스크롤하며 수집
    for _ in range(6):
        before = len(captured)
        page.capture_visible_square_images(save_dir, seen_rects, captured, use_scroll_view=True)
        if len(captured) >= 6:
            log.info("All 6 images captured.")
            break
        page.swipe_up()
        if len(captured) == before:
            log.info("No new images detected after swipe.")
            break

    log.info(f"Captured {len(captured)} images in total.")

    # 이미지 유사도 비교 (판정은 테스트에서)
    for ref in expected:
        best_score, best_path = -1, None
        for path in captured:
            screenshot = control_image.open(path).convert("RGB")
            score = control_image.compare(screenshot, ref)
            if score > best_score:
                best_score, best_path = score, path

        if best_score >= 90:
            verified_images.add(ref)
            log.info(f"[PASS] {ref} matched {best_path} ({best_score:.2f})")
        else:
            log.warning(f"[FAIL] {ref} best {best_path} ({best_score:.2f})")

    check.equal(verified_images, expected, f"[VERIFY FAIL] Some images not matched. Found: {verified_images}")


def test_image_text(wd):
    """이미지 클릭 시 표시되는 설명 문구 일치 확인"""
    page = PhotoDemoPage(wd)

    raw_device_id = wd.capabilities.get("udid") or wd.capabilities.get("deviceUDID") or "unknown_device"
    device_id = str(raw_device_id).replace(":", "_").replace("/", "_").replace("\\", "_")

    save_dir = BASE_DIR / "Result" / "image" / device_id / "test_image_text"
    save_dir.mkdir(parents=True, exist_ok=True)

    page.open_photo_demo()
    sleep(1)

    expected_texts = {
        "original_1.png": "This is a picture of: 2 tanker ships with snowy mountains in the background",
        "original_2.png": "This is a picture of: Wispy clouds in a blue sky",
        "original_3.png": "This is a picture of: English bay with snowy mountains",
        "original_4.png": "This is a picture of: The Vancouver skyline at sunrise",
        "original_5.png": "This is a picture of: A long thin cloud below mountain level",
        "original_6.png": "This is a picture of: Imposing mountains and West Vancouver"
    }

    expected_images = [str(IMAGE_DIR / name) for name in expected_texts.keys()]

    captured, seen_rects = set(), set()
    verified_texts = set()

    def capture_and_check():
        nonlocal verified_texts
        # 현재 뷰의 모든 ImageView 스캔
        elements = page.get_all_image_views()
        log.info(f"[SCAN] Found {len(elements)} ImageViews")

        win = page.get_window_size()
        win_w, win_h = win["width"], win["height"]

        for el in elements:
            r = el.rect
            x, y, w, h = r["x"], r["y"], r["width"], r["height"]
            bottom, right = y + h, x + w

            fully_visible = (x >= -10 and y >= 0 and right <= win_w + 10 and bottom <= win_h + 30)
            square_like = abs(w - h) < 20
            if not (fully_visible and square_like):
                continue

            # 중복 방지
            for (sx, sy, sw, sh) in seen_rects:
                if abs(sx - x) < 25 and abs(sy - y) < 25 and abs(sw - w) < 10 and abs(sh - h) < 10:
                    break
            else:
                # 저장
                path = save_dir / f"captured_{len(captured) + 1}.png"
                with open(path, "wb") as f:
                    f.write(el.screenshot_as_png)
                seen_rects.add((x, y, w, h))
                captured.add(str(path))
                log.info(f"[SAVE] {path.name} ({w}x{h}) at (x={x}, y={y})")

                # 원본과 매칭
                screenshot = control_image.open(path).convert("RGB")
                best_score, matched_ref = -1, None
                for ref in expected_images:
                    ref_name = os.path.basename(ref)
                    if ref_name in verified_texts:
                        continue
                    score = control_image.compare(screenshot, ref)
                    if score > best_score:
                        best_score, matched_ref = score, ref

                if best_score < 85 or matched_ref is None:
                    log.warning(f"[SKIP] {path.name} similarity too low ({best_score:.2f})")
                    continue

                matched_name = os.path.basename(matched_ref)
                expected_text = expected_texts[matched_name]
                log.info(f"[MATCH] {path.name} ↔ {matched_name} ({best_score:.2f})")

                # 다이얼로그 텍스트 조회
                page.tap_element(el)
                actual = page.get_dialog_text()
                page.close_dialog_ok()

                check.equal(actual, expected_text, f"[TEXT FAIL] {matched_name}")
                log.info(f"[TEXT PASS] {matched_name}: '{actual}'")
                verified_texts.add(matched_name)

    # 스크롤 루프
    for _ in range(6):
        before = len(verified_texts)
        capture_and_check()
        if len(verified_texts) >= len(expected_texts):
            log.info("All expected images verified. Stopping scroll.")
            break
        page.swipe_up()
        if len(verified_texts) == before:
            log.info("🔚 No new verifications after swipe. Stopping.")
            break

    check.equal(len(verified_texts), len(expected_texts),
                f"[VERIFY FAIL] Only {len(verified_texts)}/{len(expected_texts)} verified")
