pipeline {
    agent any
    parameters {
        choice(name: 'BRANCH', choices: ['main', 'dev', 'bug_fixes'], description: 'Select branch to build')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out branch: ${params.BRANCH}"
            }
        }
                  
        stage('Set up Python venv') {
            environment {
                PATH = "C:\\Users\\Tay Wen Kai\\AppData\\Local\\Programs\\Python\\Python311;${env.PATH}"
            }
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate.bat
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install ruff mypy types-Flask
                '''
            }
        }

        stage('Lint') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                ruff check .
                mypy .
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                python -m unittest discover -v
                '''
            }
        }
        stage('Test SSH') {
            steps {
                withEnv(['PATH=C:\\Windows\\System32\\OpenSSH;' + env.PATH]) {
                    sshagent(['ec2-user']) {
                        bat 'ssh -o StrictHostKeyChecking=no ec2-user@18.141.24.7 "echo Connected!"'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Build was successful!'
            bat 'echo Build success > success.txt'
        }
        failure {
            echo 'Build failed!'
        }
    }
}













































