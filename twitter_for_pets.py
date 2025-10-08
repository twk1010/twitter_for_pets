from flask import Flask
from datetime import datetime, timezone

app = Flask(__name__)

start_time = datetime.now(timezone.utc)
tweet_counter = 0

@app.route('/')
def home():
    uptime = datetime.now(timezone.utc) - start_time
    return f"Twitter for pets has been up for {uptime}\n" \
           f"There have been {tweet_counter} tweets since the last reset"

@app.route('/tweet', methods=['POST'])
def tweet():
    global tweet_counter
    tweet_counter += 1
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
