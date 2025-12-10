# 📱 Appium Automated Test Project – *The App*
---

## 🧩 Overview  
이 프로젝트는 **Appium, Python, Pytest**를 이용하여  
Appium에서 공식 배포하는 샘플 앱 **“The App”** 의 주요 기능을 자동화 테스트한 개인 프로젝트입니다.

- 테스트 결과는 **HTML Report** 형태로 시각화됩니다.  
- 각 테스트 함수의 실행 과정은 **동영상으로 기록되어 디버깅 및 검증에 활용**할 수 있습니다.  
- AWS EC2 환경에 **Jenkins CI 서버를 직접 구축**하여  
  **로컬(Windows) 테스트 환경을 원격으로 제어 및 실행**할 수 있도록 구성했습니다.  
  (Appium Server, Emulator, Pytest 환경은 Windows PC에서 구동되며, Jenkins는 원격 실행을 담당)

### CI/CD Architecture
<img width="800" height="440" alt="image" src="https://github.com/user-attachments/assets/e613fbcb-f5a6-473d-a3ad-fc6a8f4d37ad" />


---

## 📊 Test Report Example
(아래 링크를 클릭하면, 해당 리포지토리의 `tests/Result/test-reports` 경로에 있는 HTML 파일이 렌더링됩니다.)

[🔗 View Full HTML Report](https://htmlpreview.github.io/?https://github.com/leeyeonjung/appium_the_app/blob/main/tests/Result/test-reports/report_2025-10-28_15-30-01.html)<br><br>

<p align="center">
  <img width="600" alt="HTML Report Screenshot" src="https://github.com/user-attachments/assets/6f1b3fc7-b3a3-4739-8070-a269c46f4a13" />
</p>

---

## 🔍 Key Features

### 1️⃣ **Appium 자동화 테스트**
- Appium에서 공식 제공하는 *The App* 일부 기능을 테스트 케이스로 구성했습니다.  
- 각 테스트 함수의 테스트 케이스는 `testcase_excel` 디렉터리 내 **xlsm 파일**에 정의되어 있습니다.  
- 화면 전환 및 UI 요소 검증을 자동화 코드로 구현했습니다.

### 2️⃣ **Pytest 기반 모듈화 구조**
- `conftest.py` 파일에서 **Appium 드라이버 관련 fixture를 정의 및 관리**합니다.

### 3️⃣ **HTML Report & Video Recording**
- 결과는 `tests/Result/` 하위 폴더에 생성됩니다.  
  - 📊 **HTML Report** → `tests/Result/test-reports/`  
    - 전체 테스트 결과가 **시각화된 HTML 형태로 저장**됩니다.  
  - 🎥 **Video Report** → `tests/Result/video-reports/`  
    - 각 테스트 함수의 **실행 과정이 동영상으로 기록**됩니다.  
  - 🖼️ **Image Report** → `tests/Result/image/`  
    - 테스트 함수에서 인식한 이미지가 **기기 및 테스트 함수별 PNG 파일로 저장**됩니다.

### 4️⃣ **CI 환경 (Jenkins + AWS + 로컬 테스트 실행)**
- AWS EC2(Ubuntu)에 **Jenkins를 구축**하여 테스트를 원격 제어하도록 구성했습니다.  
- Jenkins는 **명령 제어 역할**을 수행하며,  
  저장소의 변경사항이 webhook을 통해 감지되면  
  이를 기반으로 **테스트 코드를 사용해 Windows 로컬 환경에서 실제 테스트를 실행**합니다.  
- 로컬 PC에는 **Appium Server, Android Emulator, Pytest 환경**이 구성되어 있으며,  
  Jenkins에서 원격 명령으로 pytest를 실행해 테스트를 수행합니다.  
- 테스트 결과(HTML Report 및 동영상)는 로컬 환경의 `tests/Result/test-reports` 폴더에 자동 생성되며,  
  Jenkins 콘솔을 통해 테스트 진행 상황을 **실시간으로 확인**할 수 있습니다.

---

## ⚙️ Tech Stack
| 구분 | 사용 기술 |
|------|------------|
| Test Framework | **Pytest**, **Appium 3.0.2**, **uiautomator2** |
| Language | **Python 3.13.7** |
| CI/CD | **Jenkins (on AWS EC2, Ubuntu)** |
| Report | **pytest-html**, **Video Recording** |
| Device | **Android Emulator / Physical Device** |

---

## 🏗️ Project Structure
```
appium_the_app/
├── app/                                         
│   └── app-release.apk                          # Appium 공식 샘플 APK (테스트 대상 앱)
│
├── appium_server/                               # Appium 서버 환경 구성
│   ├── docker-compose.yml                       # Appium Server Docker 환경 정의
│   └── entrypoint.sh                            # 컨테이너 초기화 스크립트
│
├── jenkins_test_repo/                           # Jenkins 빌드 트리거용 리포지토리
│   └── testfile.txt                             # 변경 감지용 더미 파일
│
├── testcase_excel/
│   └── (Testcase)The_App.xlsm                   # 테스트 케이스 관리용 Excel 문서
│
├── resources/
│   └── image/                                   # baseline 이미지 저장 경로
│       ├── original_1.png ~ original_6.png
│
├── src/                                         # 소스 코드 루트
│   ├── common_util/                             # 공통 유틸리티 모듈
│   │   └── control_image.py                     # SSIM 기반 이미지 비교 유틸리티
│   │
│   ├── locaters/                                # 요소 Locators 정의
│   │   ├── app_start_locaters.py                # App Start 화면 locator
│   │   ├── echo_box_locaters.py                 # Echo Box 화면 locator
│   │   ├── login_screen_locaters.py             # Login Screen locator
│   │   ├── photo_demo_locaters.py               # Photo Demo locator
│   │   └── webview_demo_locaters.py             # WebView Demo locator
│   │
│   └── pages/                                   # Page Action 정의 (click, input, get)
│       ├── app_start.py                         # App Start page object
│       ├── echo_box.py                          # Echo Box page object
│       ├── login_screen.py                      # Login Screen page object
│       ├── photo_demo.py                        # Photo Demo page object
│       └── webview_demo.py                      # WebView Demo page object
│
├── tests/                                       # 테스트 시나리오 및 검증 로직
│   ├── test_0_app_start.py                      # 앱 실행 및 초기 화면 진입 테스트
│   ├── test_1_echo_box.py                       # Echo Box 입력 및 출력 검증
│   ├── test_2_login_screen.py                   # 로그인 화면 검증
│   ├── test_4_webview_demo.py                   # WebView 페이지 테스트
│   ├── test_7_photo_demo.py                     # Photo Demo 이미지 비교 테스트
│   └── __init__.py                              # tests 패키지 인식용
│
├── conftest.py                                  # pytest 전역 설정 및 driver fixture 정의
├── requirements.txt                             # Python 의존성 패키지 목록
├── .env.example                                 # 환경 변수 템플릿
├── Jenkinsfile                                  # Jenkins 파이프라인 정의
└── README.md                                    # 프로젝트 개요 및 실행 가이드
```

---

## 🔐 Jenkins CI Server (on AWS)
| 항목 | 정보 |
|------|------|
| **Jenkins URL** | 🔗 [http://3.36.219.242:8080](http://3.36.219.242:8080) |
| **User ID** | `guest` |
| **Password** | `guest` |
| **Execution Flow** | Jenkins → Remote Windows (pytest 실행) → 로컬 환경에서 생성된 HTML Report 수집 → Jenkins에서 표시 |
| **Trigger** | GitHub Push 이벤트를 감지하여, jenkins_test_repo 디렉터리 및 하위 파일에 변경이 발생하면 테스트 코드 실행이 자동으로 트리거 |

### 🔗 GitHub 연동 & Jenkins 자동 실행 설정
- Jenkins 자동 실행 설정 : 특정 폴더의 파일이 수정되었을 경우에만 pipeline이 실행 되도록 설정
<img width="450" height="120" alt="image" src="https://github.com/user-attachments/assets/e0f3a43b-f367-4d2e-8600-3fb9204ed99b" />


<p></p>

- Github Webhook 연동
<img width="441" height="250" alt="image" src="https://github.com/user-attachments/assets/941e7bcd-4271-4f42-9563-adcfd6608ff2" />



### 🎥 Jenkins Test Demo

<video src="https://private-user-images.githubusercontent.com/121649224/501879285-89a6745e-67ec-40ea-93cc-23c8e092face.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjA1OTk4NTMsIm5iZiI6MTc2MDU5OTU1MywicGF0aCI6Ii8xMjE2NDkyMjQvNTAxODc5Mjg1LTg5YTY3NDVlLTY3ZWMtNDBlYS05M2NjLTIzYzhlMDkyZmFjZS5tcDQ_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMDE2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTAxNlQwNzI1NTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hOTM4OWUyMGZmNTVlNWI1NGNhNTEzZjYwZDYwZWRiZWQxNjJhMWI2Y2YxZTM0ZDI3Y2I4ZGUzNzhlMTRhODg5JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.fu9RpOSsIqDZrUIixgMfwHunYgW9pX0I0Paok4OK8yw"
       controls
       width="450"
       playsinline
       muted>
</video>

### ✅ Jenkins Build Success Result
<img width="320" height="97" alt="image" src="https://github.com/user-attachments/assets/6e9ab34c-ee2c-49ce-8711-98503a3ea681" />
<p></p>
<img width="295" height="235" alt="image" src="https://github.com/user-attachments/assets/cdfb437e-8da9-49ae-872a-5bbf47198a92" />


---

## ▶️ Run Locally

### 1️⃣ 환경 설정
```bash
# 필수 패키지 설치
pip install -r requirements.txt
```

### 1️⃣-1️⃣ Device Configuration (.env 파일 설정)
테스트에 사용할 기기(device) 설정은 `.env` 파일에서 관리합니다.

#### 📝 .env 파일 생성
```bash
# .env.example 파일을 .env로 복사
cp .env.example .env
```

#### 🔧 Device 설정 방법
`.env` 파일에서 `DEVICES` 환경변수를 JSON 배열 형식으로 설정합니다.

**예시 1: 단일 기기 사용**
```env
DEVICES=[{"udid": "emulator-5554", "systemPort": 8201, "server_url": "http://127.0.0.1:4725"}]
```

**예시 2: 여러 기기 사용**
```env
DEVICES=[
  {"udid": "emulator-5556", "systemPort": 8200, "server_url": "http://127.0.0.1:4723"},
  {"udid": "emulator-5554", "systemPort": 8201, "server_url": "http://127.0.0.1:4725"},
  {"udid": "emulator-5558", "systemPort": 8202, "server_url": "http://127.0.0.1:4727"}
]
```

#### ⚙️ 필수 설정 항목
각 device 설정에는 다음 항목이 필수입니다:
- **`udid`**: 기기 식별자 (예: `"emulator-5554"`, `"R58M30ABCDE"`)
- **`systemPort`**: 각 기기별 고유한 시스템 포트 (충돌 방지를 위해 서로 다른 포트 사용)
- **`server_url`**: Appium 서버 URL (각 기기별로 다른 서버를 사용할 수 있음)

#### ⚠️ 주의사항
- 각 기기의 `systemPort`는 서로 달라야 합니다.
- 여러 기기를 사용할 경우, 각각 다른 Appium 서버 인스턴스를 실행해야 할 수 있습니다.
- JSON 형식이므로 따옴표와 대괄호를 정확히 사용해야 합니다.
- 환경별로 다른 `.env` 파일을 사용하거나, 환경변수로 직접 설정할 수 있습니다.

### 2️⃣ 테스트 실행
```bash
# Pytest를 이용해 전체 테스트 실행
pytest -v

# (HTML Report 자동 생성)
결과 파일: tests/Result/test-reports/report_YYYY-MM-DD_HH-MM-SS.html
```

### 3️⃣ 개별 테스트 실행
```bash
# 특정 테스트 모듈만 실행 예시
pytest -v tests/testcase/test_2_login_screen.py
```

### 4️⃣ 결과 확인
(아래 링크를 클릭하면, 해당 리포지토리의 아래 경로로 이동합니다.)
- 📊 **HTML Report:** [tests/Result/test-reports/](https://github.com/leeyeonjung/appium_the_app/tree/main/tests/Result/test-reports)
- 🎥 **Video Report:** [tests/Result/video-reports/](https://github.com/leeyeonjung/appium_the_app/tree/main/tests/Result/video-reports)  
- 🖼️ **Image:** [tests/Result/image/](https://github.com/leeyeonjung/appium_the_app/tree/main/tests/Result/image)

---

## 💡 Future Improvement
- iOS 환경 자동화 (Appium + XCUITest)  
- **Allure Report** 적용을 통한 테스트 결과 시각화 고도화
- 테스트 케이스 Excel 연동을 통한 결과 자동 업데이트

---

## 👩‍💻 Author
**이연정 (YJ)**  
QA Engineer  
📧 **asa48284828@gmail.com**
