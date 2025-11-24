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
                bat '''
                    cd C:\\Automation\\appium_the_app
                    git fetch origin main
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
                    cd C:\\Automation\\appium_the_app
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
                    setlocal enabledelayedexpansion
                    set "REPORT_DIR=C:\\Automation\\appium_the_app\\tests\\Result\\test-reports"
                    set "LATEST="

                    if not exist "%REPORT_DIR%" (
                        echo ⚠️ Report directory not found: "%REPORT_DIR%"
                        exit /b 0
                    )

                    for /f "delims=" %%A in ('dir /b /a-d /o-d "%REPORT_DIR%\\*.html" 2^>nul') do (
                        set "LATEST=%%A"
                        goto :found
                    )

                    :found
                    if not defined LATEST (
                        echo ⚠️ No HTML report found in "%REPORT_DIR%"
                        exit /b 0
                    )

                    echo ✅ Found latest report: !LATEST!
                    copy "%REPORT_DIR%\\!LATEST!" "%WORKSPACE%\\!LATEST!" >nul
                    echo ✅ Copied !LATEST! to Jenkins workspace.
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