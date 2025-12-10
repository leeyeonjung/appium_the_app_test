// Jenkinsfile - TEST Job for Appium Tests (theapp_test)
// Agent: windows_01
// Purpose: Run Appium automated tests on Android device

pipeline {
    agent { label 'windows_01' }
    
    parameters {
        string(name: 'APK_BUILD_NUMBER', defaultValue: 'latest', description: 'APK Build Number from theapp_deploy')
        choice(name: 'APK_TYPE', choices: ['release', 'debug'], description: 'APK Type to test')
    }
    
    environment {
        // Map ANDROID_DEVICES to DEVICES for conftest.py
        DEVICES = "${env.ANDROID_DEVICES}"
        APPIUM_SERVICE = 'AppiumServer1'
        APPIUM_PORT = '4723'
        VENV_DIR = 'venv'
    }
    
    stages {
        stage('Checkout Test Code') {
            steps {
                echo '📥 Checking out test code from GitHub...'
                checkout scm
            }
        }
        
        stage('Setup Python Virtual Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                bat '''
                    rem 가상환경이 없으면 생성
                    if not exist %VENV_DIR% (
                        echo Creating new virtual environment...
                        python -m venv %VENV_DIR%
                    ) else (
                        echo Using existing virtual environment...
                    )
                    
                    rem 활성화 및 패키지 설치 (이미 있으면 스킵됨)
                    call %VENV_DIR%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Verify Environment') {
            steps {
                echo '🔍 Verifying test environment...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate
                    echo DEVICES Configuration:
                    echo %DEVICES%
                    echo.
                    echo Python version:
                    python --version
                    echo.
                    echo Installed packages:
                    pip list
                    echo.
                    echo ADB version:
                    adb --version
                '''
            }
        }
        
        stage('Copy APK from Build Job') {
            steps {
                echo "📦 Copying ${params.APK_TYPE} APK from theapp_deploy #${params.APK_BUILD_NUMBER}..."
                script {
                    bat 'if not exist app mkdir app'
                    
                    // latest 또는 특정 빌드 번호 처리
                    def buildSelector = params.APK_BUILD_NUMBER == 'latest' ? lastSuccessful() : specific(params.APK_BUILD_NUMBER)
                    
                    echo "Using selector: ${buildSelector}"
                    echo "Filter path: android/app/build/outputs/apk/${params.APK_TYPE}/app-${params.APK_TYPE}.apk"
                    
                    try {
                        copyArtifacts projectName: 'theapp_deploy',
                                      selector: buildSelector,
                                      filter: "android/app/build/outputs/apk/${params.APK_TYPE}/app-${params.APK_TYPE}.apk",
                                      target: 'app/',
                                      flatten: true
                        echo "✅ APK copied successfully"
                    } catch (Exception e) {
                        echo "❌ Failed to copy APK: ${e.message}"
                        error("Cannot find artifact from theapp_deploy. Please check if theapp_deploy build was successful.")
                    }
                }
                
                bat '''
                    echo 📱 APK file copied:
                    dir /B app\\*.apk
                    
                    echo.
                    echo File details:
                    dir app\\*.apk
                '''
            }
        }
        
        stage('Check Connected Devices') {
            steps {
                echo '📱 Checking connected Android devices...'
                bat '''
                    echo Connected devices:
                    adb devices -l
                    
                    echo.
                    echo Device information:
                    adb shell getprop ro.product.model
                    adb shell getprop ro.build.version.release
                '''
            }
        }
        
        stage('Install APK on Device') {
            steps {
                echo '📲 Installing APK on device...'
                bat """
                    echo Uninstalling previous version (if exists)...
                    adb uninstall com.appiumpro.the_app 2>nul || echo No previous installation found
                    
                    echo.
                    echo Installing app-${params.APK_TYPE}.apk...
                    adb install -r app\\app-${params.APK_TYPE}.apk
                    
                    echo.
                    echo Verifying installation...
                    adb shell pm list packages | findstr appiumpro
                """
            }
        }
        
        stage('Start Appium Server') {
            steps {
                echo '🚀 Ensuring Appium Server is running...'
                bat """
                    rem Check if service is already running
                    sc query ${APPIUM_SERVICE} | findstr RUNNING >nul
                    
                    if errorlevel 1 (
                        echo Appium service not running, starting...
                        net start ${APPIUM_SERVICE}
                        echo Waiting for Appium to be ready...
                        timeout /t 5 /nobreak
                    ) else (
                        echo ✅ Appium service already running
                    )
                    
                    echo.
                    echo Verifying Appium on port ${APPIUM_PORT}...
                    netstat -ano | findstr :${APPIUM_PORT}
                    exit /b 0
                """
            }
        }
        
        stage('Run Appium Tests') {
            steps {
                echo '🧪 Running Appium automated tests with pytest...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate
                    pytest -v --tb=short
                '''
            }
        }
        
        stage('Collect Test Results') {
            steps {
                echo '📊 Collecting test results...'
                script {
                    bat '''
                        echo 📝 Finding latest test session...
                        
                        rem Find latest session folder (by date)
                        for /f "delims=" %%D in ('dir /b /o-d /ad Result\\* 2^>nul') do (
                            set "LATEST_SESSION=%%D"
                            goto :session_found
                        )
                        :session_found
                        
                        if defined LATEST_SESSION (
                            echo ✅ Latest session: %LATEST_SESSION%
                            
                            rem Find HTML report in the session folder
                            if exist Result\\%LATEST_SESSION%\\*.html (
                                for /f "delims=" %%H in ('dir /b Result\\%LATEST_SESSION%\\*.html 2^>nul') do (
                                    set "LATEST_HTML=%%H"
                                    goto :html_found
                                )
                                :html_found
                                
                                if defined LATEST_HTML (
                                    echo 📄 Report file: %LATEST_HTML%
                                    copy "Result\\%LATEST_SESSION%\\%LATEST_HTML%" "windows_%LATEST_HTML%"
                                    echo ✅ Copied to: windows_%LATEST_HTML%
                                )
                            ) else (
                                echo ⚠️ No HTML report found in session folder
                            )
                        ) else (
                            echo ⚠️ No test session folders found
                        )
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo '📦 Archiving test artifacts...'
            
            // Archive latest HTML test report (renamed with windows_ prefix)
            archiveArtifacts artifacts: 'windows_*.html',
                             allowEmptyArchive: true,
                             fingerprint: true
            
            echo '🛑 Stopping Appium Server...'
            bat """
                net stop ${APPIUM_SERVICE} 2>nul
                if errorlevel 1 echo Appium service already stopped
                exit /b 0
            """
            
            echo '📱 Uninstalling test APK from device...'
            bat '''
                adb uninstall com.appiumpro.the_app 2>nul
                if errorlevel 1 echo App already uninstalled
                exit /b 0
            '''
        }
        success {
            echo '✅ All tests passed successfully!'
            echo "📊 Test reports are available in Build #${env.BUILD_NUMBER} artifacts"
        }
        failure {
            echo '❌ Tests failed!'
            echo 'Check the console output and test reports for details'
            bat '''
                if exist appium.log (
                    echo.
                    echo === Appium Log ===
                    type appium.log
                )
            '''
        }
        cleanup {
            echo '🧹 Cleanup completed'
        }
    }
}
