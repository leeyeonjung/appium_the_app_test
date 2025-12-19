# Mobile Test Automation (The App)

본 프로젝트는 Android 애플리케이션 모바일 QA 테스트 자동화 프로젝트입니다.

Appium + Pytest 기반의 Page Object Model(POM) 구조를 적용하여  
UI 변경에 강한 테스트 코드를 구성하였으며,  
환경변수에 따른 Device 환경에서 테스트를 수행합니다.

각 테스트 실행 결과는 HTML 리포트, 동영상, 이미지 비교 결과로 자동 기록되어  
기능 검증과 이슈 재현, 디버깅에 활용할 수 있도록 설계되었습니다.

---

## 📌 핵심 포인트

- Appium + Pytest 기반 POM 구조 적용
- 실행 이력 관리: 세션 단위 테스트 결과(리포트·영상·이미지) 자동 저장

---

## 🧭 목차

- [🎬 실행 결과](#-실행-결과)
- [🗺 파이프라인 구성도](#-파이프라인-구성도)
- [🔁 동작 흐름](#-동작-흐름)
- [🧩 기술 스택](#-기술-스택)
- [⚙️ Quick Start](#quick-start)
- [🌎 Environment Variables](#-environment-variables)
- [🗂 프로젝트 구조](#-프로젝트-구조)
- [🏗 테스트 코드 설계 (POM)](#-테스트-코드-설계-pom)
- [🚀 Jenkins 파이프라인 구성](#-jenkins-파이프라인-구성)
- [📊 테스트 산출물](#-테스트-산출물)
- [🔗 참고 링크](#-참고-링크)

---

## 🎬 실행 결과

- 파이프라인 실행 영상

https://github.com/user-attachments/assets/b0d0df64-1893-43b9-bfc5-d05c23791a4e

- Test Report 예시 ([Link](https://htmlpreview.github.io/?https://github.com/leeyeonjung/appium_the_app_test/blob/main/Result/2025-12-18_18-58-10/report_2025-12-18_18-58-10.html))
<img width="640" height="289" alt="theapp_Report" src="https://github.com/user-attachments/assets/70888b4e-811b-49fc-acee-91bb03f56c57" />

---

## 🗺 파이프라인 구성도
<img width="512" height="340" alt="theapp" src="https://github.com/user-attachments/assets/cbdf5e8b-6700-49cb-b898-683636ebd9a0" />


---

## 🔁 동작 흐름

1. App Source Repository 코드 변경
2. GitHub Webhook → Jenkins Controller 트리거
3. Application Pipeline (theapp_deploy) 실행 → APK 빌드
4. 빌드된 APK Jenkins 아카이브 저장
5. Test Pipeline (theapp_test) 실행 → 빌드 APK 기반 테스트 수행
6. 테스트 리포트 Jenkins 아카이브 및 이력 관리

---

## 🧩 기술 스택

| 구분 | 기술 |
|---|---|
| Test Framework | Pytest, pytest-html |
| Mobile Automation | Appium 3.0.2 |
| Android Driver | uiautomator2 |
| Language | Python 3.13 |
| Config | python-dotenv |
| Device | Android Emulator / Physical Device |

---

<a name="quick-start"></a>
## ⚙️ Quick Start

```bash
pip install -r requirements.txt
pytest -v
```

---

## 🌎 Environment Variables

### ✔ Device 설정 예시

```env
DEVICES=[{"udid":"emulator-5554","systemPort":8201,"server_url":"http://127.0.0.1:4725"}]
```

---

## 🗂 프로젝트 구조

```text
appium_the_app/
├── app/
│   └── app-release.apk          # 테스트 대상 Android 앱(APK)
├── testcase_excel/
│   └── (Testcase)The_App.xlsm    # 테스트 케이스 정의 문서
├── resources/
│   └── image/                   # 테스트용 이미지 리소스
├── src/
│   ├── common_util/             # 공통 유틸리티
│   │   └── control_image.py     # 이미지 처리/제어 로직
│   ├── locaters/                # 화면 요소 locator 정의
│   └── actions/                 # 화면 동작(Action) 정의
├── tests/
│   ├── test_00_app_start.py      # 앱 실행 테스트
│   ├── test_01_echo_box.py       # Echo Box 기능 테스트
│   ├── test_02_login_screen.py   # 로그인 화면 테스트
│   ├── test_04_webview_demo.py   # WebView 테스트
│   └── test_07_photo_demo.py     # 사진/이미지 기능 테스트
├── conftest.py                  # pytest/Appium 공통 설정
├── requirements.txt             # 의존성 목록
├── .env.example                 # 환경 변수 템플릿
└── README.md                    # 프로젝트 설명
```

---

## 🏗 테스트 코드 설계 (POM)

POM 구조를 적용하여 UI 변경에 강한 테스트 코드 구조를 유지했습니다.  

### 구성 요소

- Actions: 비즈니스 동작 정의 (`src/actions/`)  
- Locators: UI 선택자 관리 (`src/locators/`)  
- Utils: 환경·토큰 공통 모듈 (`src/common_util/`)  
- Tests: 테스트 시나리오 (`tests/`)  

---

## 🚀 Jenkins 파이프라인 구성
- Jenkins: http://3.36.219.242:8080 (ID: guest / PW: guest)
(상세 링크 하단 [🔗 참고 링크](#-참고-링크) 참조)

### 🔹 Application Pipeline (`theapp_deploy`)
- main 브랜치 변경 감지
- Android App APK 빌드
- 빌드된 APK Jenkins 아카이브 저장

### 🔹 Test Pipeline (`theapp_test`)
- `theapp_deploy`에서 생성된 APK 아티팩트 수신
- 환경 변수 설정 기기 대상 모바일 테스트 실행 (pytest 기반)
- HTML 테스트 리포트 생
- 테스트 결과 Jenkins 아카이브 및 이력 관리

---

## 🧪 테스트 자동화 범위

- App Start 화면 검증
- Echo Box 기능 검증
- Login Screen UI 검증
- WebView 로딩 테스트
- Photo Demo 이미지 비교 (SSIM)

---

## 📊 테스트 산출물
- [Example Link](https://github.com/leeyeonjung/appium_the_app_test/tree/main/Result)

- 저장 위치 `Result/{YYYY-MM-DD_HH-MM-SS}/`
  - HTML 리포트
  - 실행 로그
  - 테스트별 동영상

---

## 🔗 참고 링크

- 테스트 대상 앱: Appium 공식 샘플 앱 The App
- App Source Repository: https://github.com/leeyeonjung/appium_the_app
- Jenkins: http://3.36.219.242:8080 (ID: guest / PW: guest)  
  - `theapp_deploy`: http://3.36.219.242:8080/view/theapp/job/theapp_deploy/  
  - `theapp_test`: http://3.36.219.242:8080/view/theapp/job/theapp_test/
