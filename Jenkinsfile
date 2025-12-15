// Jenkinsfile - TEST Job for Appium Tests (theapp_test)
// Agent: windows_01
// Purpose: Run Appium automated tests on Android device

pipeline {
    agent { label 'windows_01' }
    
    parameters {
        string(name: 'APK_BUILD_NUMBER', defaultValue: 'latest', description: 'APK Build Number from theapp_deploy')
        string(name: 'APK_TYPE', defaultValue: 'release', description: 'APK Type (fixed to release)')
    }
    
    environment {
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
                    if not exist %VENV_DIR% (
                        python -m venv %VENV_DIR%
                    )
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
                    python --version
                    adb --version
                    python -c "import json, os; devices = json.loads(os.getenv('DEVICES', '[]')); print(devices[0]['udid'] if devices else 'emulator-5554', end='')" > device_id.txt
                '''
            }
        }
        
        stage('Copy APK from Build Job') {
            steps {
                echo "📦 Copying APK from theapp_deploy #${params.APK_BUILD_NUMBER}..."
                script {
                    bat 'if not exist app mkdir app'
                    
                    def buildSelector = params.APK_BUILD_NUMBER == 'latest' ? lastSuccessful() : specific(params.APK_BUILD_NUMBER)
                    
                    try {
                        copyArtifacts projectName: 'theapp_deploy',
                                      selector: buildSelector,
                                      filter: "android/app/build/outputs/apk/${params.APK_TYPE}/app-${params.APK_TYPE}.apk",
                                      target: 'app/',
                                      flatten: true
                    } catch (Exception e) {
                        error("Cannot find artifact from theapp_deploy build #${params.APK_BUILD_NUMBER}")
                    }
                }
            }
        }
        
        stage('Verify Device Configuration') {
            steps {
                echo '📱 Verifying target device...'
                bat '''
                    set /p DEVICE_ID=<device_id.txt
                    adb -s %DEVICE_ID% shell getprop ro.product.model
                    adb -s %DEVICE_ID% shell getprop ro.build.version.release
                '''
            }
        }
        
        stage('Install APK on Device') {
            steps {
                echo '📲 Installing APK on device...'
                bat """
                    set /p DEVICE_ID=<device_id.txt
                    adb -s %DEVICE_ID% uninstall com.appiumpro.the_app 2>nul
                    adb -s %DEVICE_ID% install -r app\\app-${params.APK_TYPE}.apk
                    adb -s %DEVICE_ID% shell pm list packages | findstr appiumpro
                """
            }
        }
        
        stage('Start Appium Server') {
            steps {
                echo '🚀 Starting Appium Server...'
                bat '''
                    sc query AppiumServer1 | findstr /C:"RUNNING" >nul 2^>^&1
                    if errorlevel 1 (
                        net start AppiumServer1
                        powershell -command "Start-Sleep -Seconds 10"
                    )
                '''
            }
        }
        
        stage('Run Appium Tests') {
            steps {
                echo '🧪 Running Appium tests...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate
                    pytest -v tests\\test_00_app_start.py --tb=short
                '''
            }
        }
    }
    
    post {
        always {
            script {
                bat '''
                    @echo off
                    if exist Result (
                        powershell -Command "& { $session = Get-ChildItem Result -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if ($session) { $html = Get-ChildItem $session.FullName -Filter *.html | Select-Object -First 1; if ($html) { $target = 'windows_' + $html.Name; Copy-Item $html.FullName $target -Force } } }"
                    )
                    exit /b 0
                '''
            }
            
            archiveArtifacts artifacts: 'windows_*.html',
                             allowEmptyArchive: true,
                             fingerprint: true
            
            bat '''
                net stop AppiumServer1 2>nul
                exit /b 0
            '''
            
            bat '''
                if exist device_id.txt (
                    set /p DEVICE_ID=<device_id.txt
                    adb -s %DEVICE_ID% uninstall com.appiumpro.the_app 2>nul
                ) else (
                    adb uninstall com.appiumpro.the_app 2>nul
                )
                exit /b 0
            '''
        }
        success {
            echo '✅ All tests passed!'
        }
        failure {
            echo '❌ Tests failed! Check console output for details'
            bat '''
                if exist appium.log type appium.log
            '''
        }
    }
}
