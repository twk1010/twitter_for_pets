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
                        sshagent(['key-06087a0873dcffa60']) {
                            sh 'ssh -o StrictHostKeyChecking=no ec2-user@18.141.12.169 "echo hello"'
               }
            }
        }
        stage('Deploy') {
            when {
                tag "release-*"
            }
            steps {
                sshagent(['key-06087a0873dcffa60']) { // Jenkins SSH credential ID
                    sh '''
                    ssh -o StrictHostKeyChecking=no ec2-user@18.141.12.169 << 'ENDSSH'

                    # Set deployment directory
                    DEPLOY_DIR=~/twitter_for_pets
                    mkdir -p $DEPLOY_DIR
                    cd $DEPLOY_DIR

                    # Stop old server if running (don't fail if not running)
                    pkill -f twitter_for_pets.py || true

                    # Copy updated files from Jenkins workspace
                    scp -o StrictHostKeyChecking=no USER@JENKINS_SERVER_IP:/path/to/workspace/twitter_for_pets.py .
                    scp -o StrictHostKeyChecking=no USER@JENKINS_SERVER_IP:/path/to/workspace/requirements.txt .

                    # Setup Python virtual environment
                    if [ ! -d "venv" ]; then
                        python3 -m venv venv
                    fi

                    # Activate venv and install requirements
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    # Run the server in the background
                    nohup python twitter_for_pets.py > twitter_for_pets.log 2>&1 &

                    ENDSSH
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


























