pipeline {
    agent { label 'windows' }

    stages {
        /*
        // 이전 Jenkinsfile의 'Skip Info' 스테이지는 이제 필요 없습니다.
        // Jenkins가 애초에 빌드를 시작하지 않기 때문입니다.
        stage('Skip Info') {
            ...
        }
        */

        // Checkout Test Code 스테이지는 주석 처리된 상태로 유지합니다.
        stage('Checkout Test Code') {
            steps {
                echo "📦 Updating local appium_the_app repository..."
                bat '''
                    cd C:\\appium_the_app
                    git fetch origin main
                    git reset --hard origin/main
                '''
            }
        }

        stage('Run Pytest on Windows') {
            steps {
                echo "🚀 Running pytest..."
                bat '''
                    cd C:\\appium_the_app
                    pytest -v --maxfail=1 --disable-warnings 
                '''
            }
        }

    }

    post {
        always {
            script {
                // 더 이상 ABORTED 상태를 확인할 필요가 없습니다.
                // if (currentBuild.result == 'ABORTED') {
                //     echo "⏩ Post block skipped (build was aborted)."
                //     return
                // }

                echo "📊 Collecting latest HTML report..."

                // ✅ 최신 HTML 1개만 Jenkins 워크스페이스로 복사 (파일명 변경 없음)
                bat '''
                    setlocal enabledelayedexpansion
                    set "REPORT_DIR=C:\\appium_the_app\\tests\\Result\\test-reports"
                    set "LATEST="

                    if not exist "%REPORT_DIR%" (
                        echo ⚠️ Report directory not found: "%REPORT_DIR%"
                        exit /b 0
                    )

                    REM 최신순으로 정렬 후 첫 번째(가장 최근) 파일만 선택
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
                archiveArtifacts artifacts: '*.html', fingerprint: true, onlyIfSuccessful: false
            }
        }
    }
}