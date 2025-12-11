import os
import json
import base64
import logging
from datetime import datetime
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from src.common_util import env_loader

log = logging.getLogger(__name__)

env_loader.load_env_files()

SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def load_devices_from_env():
    devices_json = env_loader.getenv("DEVICES", "[]")
    devices_list = json.loads(devices_json)

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


@pytest.fixture(autouse=True)
def record_video(request, wd):
    file_name = Path(request.node.fspath).stem
    raw_device_id = wd.capabilities.get("udid") or wd.capabilities.get("deviceUDID") or "unknown_device"
    device_id = str(raw_device_id).replace(":", "_").replace("/", "_").replace("\\", "_")

    save_dir = Path(__file__).resolve().parents[0] / "Result" / SESSION_TIMESTAMP / "video-reports" / device_id / file_name
    os.makedirs(save_dir, exist_ok=True)

    test_name = request.node.originalname or request.node.name
    safe_name = "".join(c for c in test_name if c.isalnum() or c in ("_", "-"))
    save_path = save_dir / f"{safe_name}.mp4"

    wd.start_recording_screen()
    yield
    video_raw = wd.stop_recording_screen()

    with open(save_path, "wb") as f:
        f.write(base64.b64decode(video_raw))

    log.info(f"[VIDEO] {device_id} → {safe_name} 실행 동영상 저장 완료 → {save_path}")


def pytest_configure(config):
    if not getattr(config.option, "htmlpath", None):
        report_dir = Path(__file__).resolve().parents[0] / "Result" / SESSION_TIMESTAMP
        report_dir.mkdir(parents=True, exist_ok=True)

        report_path = report_dir / f"report_{SESSION_TIMESTAMP}.html"

        config.option.htmlpath = str(report_path)
        config.option.self_contained_html = True
