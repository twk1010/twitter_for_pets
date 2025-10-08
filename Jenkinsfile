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
                pip install ruff mypy
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

        stage('Deploy') {
            when {
                tag "release-*"
            }
            steps {
                echo "Running deployment to production..."
                sshagent (credentials: ['prod_ssh_key']) {
                    bat '''
                    set "PROD_IP=<PROD_SERVER_IP>"

                    rem Kill any running twitter_for_pets.py process
                    ssh -o StrictHostKeyChecking=no ubuntu@%PROD_IP% "pkill -f twitter_for_pets.py || true"

                    rem Copy the files to production
                    pscp -r twitter_for_pets.py requirements.txt ubuntu@%PROD_IP%:~/twitter_for_pets/

                    rem Run remote setup and restart
                    ssh ubuntu@%PROD_IP% "cd ~/twitter_for_pets && \
                        python3 -m venv venv || true && \
                        source venv/bin/activate && \
                        pip install -r requirements.txt && \
                        nohup python3 twitter_for_pets.py > server.log 2>&1 &"
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













