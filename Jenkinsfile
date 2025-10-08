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

        stage('Deploy') {
            when {
                tag "release-*"
            }
            steps {
                dir('repo') {
                    withCredentials([
                        sshUserPrivateKey(
                            credentialsId: 'jenkins-ssh-key',
                            keyFileVariable: 'SSH_KEY',
                            usernameVariable: 'SSH_USER'
                        )
                    ]) {
                        bat '''
                        echo --- Starting Deployment ---
                        set "SERVER_IP=<PROD_SERVER_IP>"
                        set "SSH_CMD=ssh -i %SSH_KEY% -o StrictHostKeyChecking=no %SSH_USER%@%SERVER_IP%"
                        set "SCP_CMD=scp -i %SSH_KEY% -o StrictHostKeyChecking=no"

                        echo --- Killing any running twitter_for_pets.py ---
                        %SSH_CMD% "pkill -f twitter_for_pets.py || true"

                        echo --- Copying updated source files ---
                        %SCP_CMD% twitter_for_pets.py requirements.txt %SSH_USER%@%SERVER_IP%:~/twitter_for_pets/

                        echo --- Creating venv if missing ---
                        %SSH_CMD% "cd ~/twitter_for_pets && python3 -m venv venv || true"

                        echo --- Installing dependencies ---
                        %SSH_CMD% "cd ~/twitter_for_pets && ./venv/bin/pip install --upgrade pip && ./venv/bin/pip install -r requirements.txt"

                        echo --- Starting server in background ---
                        %SSH_CMD% "cd ~/twitter_for_pets && nohup ./venv/bin/python twitter_for_pets.py > server.log 2>&1 &"

                        echo --- Deployment complete ---
                        '''
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























