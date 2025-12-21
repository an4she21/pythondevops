pipeline {
    agent any

    environment {
        IMAGE_NAME = "pythonflask:latest"
        CONTAINER_NAME = "pythonflask-container"
        HOST_PORT = "8081"
        CONTAINER_PORT = "5000"
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
                bat """
                cd tests
                python -m unittest discover -p "test_*.py"
                """
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
            echo "🚀 Flask app deployed in Docker!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}

