pipeline {
    agent any

    environment {
        IMAGE_NAME = "pythonflask:latest"
        CONTAINER_NAME = "pythonflask-container"
        HOST_PORT = "8081"
        CONTAINER_PORT = "5000"
        SONAR_PROJECT_KEY = "pythondevops-project"
        SONAR_SCANNER_HOME = tool 'SonarScanner'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/an4she21/pythondevops.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r src/requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m unittest discover -p "test_*.py"'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat """
                    %SONAR_SCANNER_HOME%\\bin\\sonar-scanner ^
                    -Dsonar.projectKey=%SONAR_PROJECT_KEY% ^
                    -Dsonar.sources=src ^
                    -Dsonar.language=py
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Deploy (Local Docker)') {
            steps {
                bat '''
                docker stop %CONTAINER_NAME% || exit 0
                docker rm %CONTAINER_NAME% || exit 0
                docker run -d --name %CONTAINER_NAME% -p %HOST_PORT%:%CONTAINER_PORT% %IMAGE_NAME%
                '''
            }
        }
    }

    post {
        success {
            echo "TP4 SUCCES : SonarQube + Tests + Docker"
        }
        failure {
            echo " Pipeline "
        }
    }
}
