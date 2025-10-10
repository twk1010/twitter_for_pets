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
                sshagent(['ec2-user']) {
                    bat 'ssh -o StrictHostKeyChecking=no ec2-user@13.229.116.91 "echo Connected!"'
                }
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['ec2-user']) { // Jenkins SSH credential ID
                    bat '''
                    REM Copy all files to EC2 instance
                    scp -o StrictHostKeyChecking=no -r * ec2-user@13.229.116.91:~/twitter_for_pets
        
                    REM Run remote restart on EC2
                    ssh -o StrictHostKeyChecking=no ec2-user@13.229.116.91 ^
                    bash -c "'cd ~/twitter_for_pets && pkill -f twitter_for_pets.py || true && nohup python3 twitter_for_pets.py > app.log 2>&1 & echo Deployment complete'"
                    '''
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





















































