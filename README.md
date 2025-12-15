# The App Test Automation

이 테스트 자동화 프로젝트는 **Appium과 Pytest 기반 POM(Page Object Model)** 구조를 적용하여  
Android 애플리케이션의 UI 동작을 체계적으로 검증하도록 설계된 **모바일 QA 테스트 스택**입니다.  

Appium에서 공식 제공하는 샘플 앱 **“The App”** 을 테스트 대상으로 하며,  
실제 Emulator 및 Physical Device 환경에서 테스트를 수행하고  
테스트 결과는 **HTML 리포트·동영상·이미지** 형태로 자동 기록되어  
기능 검증과 디버깅에 활용됩니다.

---

## 🧩 기술 스택

- Pytest / pytest-html  
- Appium 3.0.2 / uiautomator2  
- Python 3.13  
- python-dotenv  
- Android Emulator / Physical Device  

---

## 🏗 Page Object Model (POM)

### 구성 요소
- **Actions**: 화면 단위 사용자 액션 정의 (`src/actions/`)  
- **Locators**: UI 요소 선택자 정의 (`src/locaters/`)  
- **Utils**: 이미지 비교 및 공통 유틸 (`src/common_util/`)  
- **Tests**: 테스트 시나리오 및 검증 로직 (`tests/`)  

### 설계 원칙
- Page Object는 **행위만 담당** (click / input / get)  
- 모든 검증(assert)은 `tests/` 에서만 수행  
- 화면·기능 단위로 코드 책임을 명확히 분리  

---

## 🗂 프로젝트 구조

```
appium_the_app/
├── app/
│   └── app-release.apk                 # 테스트 대상 APK
│
├── testcase_excel/
│   └── (Testcase)The_App.xlsm           # 테스트 케이스 관리 문서
│
├── resources/
│   └── image/                           # 기준 이미지 (SSIM 비교)
│
├── src/
│   ├── common_util/
│   │   └── control_image.py             # 이미지 비교 유틸
│   ├── locaters/                        # 화면별 locator 정의
│   └── actions/                         # Page Object (행위 정의)
│
├── tests/
│   ├── test_0_app_start.py
│   ├── test_1_echo_box.py
│   ├── test_2_login_screen.py
│   ├── test_4_webview_demo.py
│   ├── test_7_photo_demo.py
│   └── __init__.py
│
├── conftest.py                          # Appium driver fixture
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧪 테스트 자동화 범위

### UI 기능 검증
- App Start 화면 진입
- Echo Box 입력/출력 동작 검증
- Login Screen UI 요소 검증
- WebView 페이지 로딩 및 상호작용
- Photo Demo 이미지 비교 (SSIM 기반)

### 테스트 케이스 관리
- 테스트 시나리오는 **Excel(xlsm)** 기반으로 관리 (testcases_excel/(Testcase)The_App.xlsm)  

---

## 🌎 환경 변수 설정

### ✔ 관리 방식
- 환경 변수는 `.env` 파일을 통해 관리  
- 다중 디바이스 실행을 고려하여 JSON 배열 형태로 설정  

### ✔ Device 설정 예시

**단일 기기**
```env
DEVICES=[{"udid":"emulator-5554","systemPort":8201,"server_url":"http://127.0.0.1:4725"}]
```

**다중 기기**
```env
DEVICES=[
  {"udid":"emulator-5556","systemPort":8200,"server_url":"http://127.0.0.1:4723"},
  {"udid":"emulator-5554","systemPort":8201,"server_url":"http://127.0.0.1:4725"}
]
```

---

## 📊 테스트 리포트

모든 테스트 실행 결과는 다음 경로에 세션 단위로 저장됩니다.

```
Result/{YYYY-MM-DD_HH-MM-SS}/
```

### 포함 내용
- 테스트 통과/실패 요약  
- 테스트 실행 시간  
- 실행 로그  
- 테스트 함수 단위 동영상  
- 이미지 비교 결과  

---

## ⚙️ 설치 및 실행 방법

### 1) 의존성 설치
```bash
pip install -r requirements.txt
```

### 2) 테스트 실행
```bash
pytest -v
```

(HTML 리포트 자동 생성)

---
