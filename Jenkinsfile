pipeline {
    agent any 
    environment {
        DOCKER_HUB = 'cithit/pyakurh2' 
        TAG = "lab5.1-${BUILD_NUMBER}"
        KUBECONFIG = credentials('pyakurh2-sp26') 
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Linting') {
            steps {
                sh 'python3 -m pip install flake8'
                sh 'python3 -m flake8 main.py --ignore=E501'
            }
        }
        stage('Static Security Scan') {
            steps {
                sh 'python3 -m pip install bandit'
                sh 'python3 -m bandit -r main.py'
            }
        }
        stage('Docker Build & Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'roseaw-dockerhub') {
                        def img = docker.build("${DOCKER_HUB}:${TAG}")
                        img.push()
                        img.push("latest")
                    }
                }
            }
        }
        stage('Deploy to K8s') {
            steps {
                sh "sed -i 's|IMAGE_PLACEHOLDER|${DOCKER_HUB}:${TAG}|' deployment-dev.yaml"
                sh "kubectl apply -f deployment-dev.yaml"
            }
        }
    }
}
