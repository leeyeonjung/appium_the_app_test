# conftest.py

# Standard library
import os
import json
import base64
import logging
from datetime import datetime
from pathlib import Path

# Third-party libraries
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# Local modules
from src.common_util import env_loader

log = logging.getLogger(__name__)

# 환경 변수 파일 로드
env_loader.load_env_files()


# 📱 Device Configuration
def load_devices_from_env():
    """환경변수에서 devices 설정을 로드합니다."""
    devices_json = env_loader.getenv("DEVICES", "[]")
    devices_list = json.loads(devices_json)

    # pytest.param 리스트로 변환
    devices = []
    for device_config in devices_list:
        device_id = device_config.get("udid", "unknown")
        devices.append(
            pytest.param(
                {
                    "udid": device_config["udid"],
                    "systemPort": device_config["systemPort"],
                    "server_url": device_config["server_url"]
                },
                id=device_id
            )
        )

    return devices


devices = load_devices_from_env()


# 📱 Appium Driver 설정
@pytest.fixture(params=devices)
def wd(request):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.udid = request.param["udid"]
    options.system_port = request.param["systemPort"]
    options.app_package = "com.appiumpro.the_app"
    options.app_activity = "com.appiumpro.the_app.MainActivity"
    options.auto_grant_permissions = True
    options.no_reset = False

    driver = webdriver.Remote(request.param["server_url"], options=options)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


# 🎥 Test Video Recording Fixture
@pytest.fixture(autouse=True)  # 비디오 녹화 불필요시 autouse=False 변경하여 사용 가능.
def record_video(request, wd):

    # 테스트 스크립트 파일명
    file_name = Path(request.node.fspath).stem

    # 기기 식별자
    raw_device_id = wd.capabilities.get("udid") or wd.capabilities.get("deviceUDID") or "unknown_device"
    device_id = str(raw_device_id).replace(":", "_").replace("/", "_").replace("\\", "_")

    # === Result/video-reports/{device_id}/{테스트 파일명}/ ===
    save_dir = Path(__file__).resolve().parents[0] / "Result" / "video-reports" / device_id / file_name
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    test_name = request.node.originalname or request.node.name
    safe_name = "".join(c for c in test_name if c.isalnum() or c in ("_", "-"))

    save_path = save_dir / f"{safe_name}_{timestamp}.mp4"

    wd.start_recording_screen()
    yield
    video_raw = wd.stop_recording_screen()

    with open(save_path, "wb") as f:
        f.write(base64.b64decode(video_raw))

    log.info(f"[VIDEO] {device_id} → {safe_name} 실행 동영상 저장 완료 → {save_path}")


# 📊 pytest 실행 시 항상 HTML Report 자동 생성
def pytest_configure(config):
    # --html 옵션 없어도 자동으로 생성
    if not getattr(config.option, "htmlpath", None):
        report_dir = Path(__file__).resolve().parents[0] / "Result" / "test-reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = report_dir / f"report_{timestamp}.html"

        # 옵션 주입
        config.option.htmlpath = str(report_path)
        config.option.self_contained_html = True
