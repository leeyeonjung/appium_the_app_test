pipeline {
    agent { label 'mobile_windows' }

    stages {

        stage('Checkout Test Code') {
            steps {
                echo "Syncing appium_the_app..."
                bat '''
                    cd C:\\Automation\\appium_the_app
                    git fetch --all
                    git reset --hard origin/main
                '''
            }
        }

        stage('Run Pytest on Windows') {
            steps {
                echo "Running pytest..."
                bat '''
                    cd C:\\Automation\\appium_the_app
                    pytest -v
                '''
            }
        }
    }

    post {
        always {
            echo "📊 Collecting latest HTML report..."
            bat '''
                setlocal enabledelayedexpansion
                set "REPORT_DIR=C:\\Automation\\appium_the_app\\tests\\Result\\test-reports"
                set "LATEST="

                if not exist "%REPORT_DIR%" exit /b 0

                for /f "delims=" %%A in ('dir /b /a-d /o-d "%REPORT_DIR%\\*.html" 2^>nul') do (
                    set "LATEST=%%A"
                    goto :found
                )

                :found
                if not defined LATEST exit /b 0

                copy "%REPORT_DIR%\\!LATEST!" "%WORKSPACE%\\!LATEST!"
                endlocal
            '''

            archiveArtifacts artifacts: '*.html', fingerprint: true
        }
    }
}
