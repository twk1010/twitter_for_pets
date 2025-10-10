#!/bin/bash
set -e

DEPLOY_DIR=~/twitter_for_pets
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Stop old app
pkill -f twitter_for_pets.py || true

# Setup Python venv
if [ ! -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start app in background
nohup python3 twitter_for_pets.py > app.log 2>&1 &

echo "Deployment complete. Logs at $DEPLOY_DIR/app.log"