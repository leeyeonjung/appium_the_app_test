pipeline {
    // Windows 에이전트에서 실행
    // label 'windows'로 지정된 Jenkins 노드에서 파이프라인이 실행됩니다
    agent { label 'windows' }

    // 파이프라인의 실행 단계들을 정의
    stages {

        // Stage 1: 테스트 코드 체크아웃
        // 최신 코드를 가져와서 로컬 저장소를 업데이트합니다
        stage('Checkout Test Code') {
            steps {
                echo "📦 Updating local appium_the_app repository..."
                // Windows 배치 스크립트 실행
                bat '''
                    // 작업 디렉토리로 이동
                    cd C:\\appium_the_app
                    // 원격 저장소의 main 브랜치 최신 변경사항 가져오기
                    git fetch origin main
                    // 로컬 저장소를 원격 main 브랜치와 완전히 동기화 (로컬 변경사항 무시)
                    git reset --hard origin/main
                '''
            }
        }

        // Stage 2: Pytest 실행
        // Appium 테스트 케이스들을 실행합니다
        stage('Run Pytest on Windows') {
            steps {
                echo "🚀 Running pytest..."
                bat '''
                    // 테스트 디렉토리로 이동
                    cd C:\\appium_the_app
                    // pytest 실행 옵션:
                    // -v: 상세 출력 (verbose)
                    // --maxfail=1: 첫 번째 실패 후 중단
                    // --disable-warnings: 경고 메시지 비활성화
                    pytest -v --maxfail=1 --disable-warnings 
                '''
            }
        }

    }

    // 파이프라인 실행 후 항상 실행되는 후처리 단계
    // 성공/실패 여부와 관계없이 리포트를 수집합니다
    post {
        always {
            script {

                echo "📊 Collecting latest HTML report..."

                // Windows 배치 스크립트로 최신 HTML 리포트 찾기 및 복사
                bat '''
                    // 지연된 변수 확장 활성화 (변수 값을 동적으로 사용하기 위함)
                    setlocal enabledelayedexpansion
                    // 리포트가 저장된 디렉토리 경로 설정
                    set "REPORT_DIR=C:\\appium_the_app\\tests\\Result\\test-reports"
                    // 최신 리포트 파일명을 저장할 변수 초기화
                    set "LATEST="

                    // 리포트 디렉토리가 존재하는지 확인
                    if not exist "%REPORT_DIR%" (
                        echo ⚠️ Report directory not found: "%REPORT_DIR%"
                        // 디렉토리가 없어도 에러 없이 종료
                        exit /b 0
                    )

                    // 최신순으로 정렬 후 첫 번째(가장 최근) 파일만 선택
                    // dir /b: 파일명만 출력, /a-d: 디렉토리 제외, /o-d: 수정일시 내림차순 정렬
                    // 2^>nul: 에러 메시지 숨김
                    for /f "delims=" %%A in ('dir /b /a-d /o-d "%REPORT_DIR%\\*.html" 2^>nul') do (
                        set "LATEST=%%A"
                        // 첫 번째 파일을 찾으면 루프 종료
                        goto :found
                    )

                    :found
                    // 리포트 파일이 없는 경우 처리
                    if not defined LATEST (
                        echo ⚠️ No HTML report found in "%REPORT_DIR%"
                        exit /b 0
                    )

                    // 최신 리포트 파일을 찾았음을 알림
                    echo ✅ Found latest report: !LATEST!
                    // 최신 리포트를 Jenkins 워크스페이스로 복사
                    // >nul: 복사 메시지 숨김
                    copy "%REPORT_DIR%\\!LATEST!" "%WORKSPACE%\\!LATEST!" >nul
                    echo ✅ Copied !LATEST! to Jenkins workspace.
                    // 로컬 변수 환경 종료
                    endlocal
                '''

                echo "📤 Archiving only the latest HTML report..."
                // HTML 리포트 파일을 Jenkins 아티팩트로 아카이빙
                // artifacts: '*.html': 워크스페이스의 모든 HTML 파일
                // fingerprint: true: 파일 지문 생성 (빌드 추적용)
                // onlyIfSuccessful: false: 실패한 빌드에서도 아카이빙
                archiveArtifacts artifacts: '*.html', fingerprint: true, onlyIfSuccessful: false
            }
        }
    }
}