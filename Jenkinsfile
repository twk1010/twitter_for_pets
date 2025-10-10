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
            steps {
                sshagent(['ec2-user']) { // Jenkins SSH credential ID
                    bat '''
                    REM Copy all files to EC2 instance
                    scp -o StrictHostKeyChecking=no -r * ec2-user@13.229.116.91:~/twitter_for_pets
        
                    REM Run remote restart on EC2
                    ssh -o StrictHostKeyChecking=no ec2-user@13.229.116.91 ^
                    "bash -lc '
                        set -e  # stop if any command fails
        
                        echo \"Deploying Twitter app...\"
        
                        # Go to deployment directory
                        mkdir -p ~/twitter_for_pets
                        cd ~/twitter_for_pets
        
                        # Stop old app if running (ignore errors)
                        pkill -f twitter_for_pets.py || true
        
                        # Setup virtual environment if not exists
                        if [ ! -d venv ]; then
                            python3 -m venv venv
                        fi
        
                        # Activate venv
                        source venv/bin/activate
        
                        # Install dependencies
                        pip install --upgrade pip
                        pip install -r requirements.txt
        
                        # Start the app in background and redirect logs
                        nohup python3 twitter_for_pets.py > app.log 2>&1 &
        
                        echo \"Deployment complete. Logs at ~/twitter_for_pets/app.log\"
                    '"
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






















































