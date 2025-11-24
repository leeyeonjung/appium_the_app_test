pipeline {
    agent { label 'windows' }

    stages {

        // ============================
        // Stage 0: 변경된 파일 확인
        // ============================
        stage('Check Changed Files') {
            steps {
                script {
                    echo "🔍 Checking if jenkins_test_repo/ has changes..."

                    def changed = false

                    // GitHub Webhook으로 전달된 changeSet 확인
                    for (change in currentBuild.changeSets) {
                        for (item in change.items) {
                            for (file in item.affectedFiles) {
                                echo "Changed file: ${file.path}"
                                if (file.path.startsWith("jenkins_test_repo/")) {
                                    changed = true
                                }
                            }
                        }
                    }

                    if (!changed) {
                        echo "⏳ No changes in jenkins_test_repo/. Entire pipeline skipped."

                        // 파이프라인 상태 지정
                        currentBuild.result = 'NOT_BUILT'

                        // 파이프라인 전체 종료 (ERROR 출력 없이 종료)
                        throw new org.jenkinsci.plugins.workflow.steps.FlowInterruptedException(
                            org.jenkinsci.plugins.workflow.steps.FlowInterruptedException.Result.NOT_BUILT
                        )
                    }

                    echo "✅ Change detected in jenkins_test_repo/. Continuing pipeline..."
                }
            }
        }

        // ============================
        // Stage 1: 테스트 코드 체크아웃
        // ============================
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

        // ============================
        // Stage 2: Pytest 실행
        // ============================
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

    post {
        always {
            script {
                echo "📊 Collecting latest HTML report..."

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
                archiveArtifacts artifacts: '*.html', fingerprint: true, onlyIfSuccessful: false
            }
        }
    }
}
