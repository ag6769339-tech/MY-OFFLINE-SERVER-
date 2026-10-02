import os
import time
import requests
import string
import random
from flask import Flask, request, render_template_string
from threading import Thread, Event

app = Flask(__Arslan__)

stop_events = {}

def send_messages(tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events.get(task_id)
    while stop_event and not stop_event.is_set():
        for token in tokens:
            for message in messages:
                if stop_event and stop_event.is_set():
                    break
                url = f"https://graph.facebook.com/v15.0/t_{thread_id}/"
                parameters = {
                    'access_token': token,
                    'message': f"{mn} {message}" if mn else message
                }
                response = requests.post(url, data=parameters)
                if response.status_code == 200:
                    print(f"[ARSLAN GILL SERVER] [+] Message sent: {message}")
                else:
                    print(f"[ARSLAN GILL SERVER] [-] Failed to send: {response.text}")
                time.sleep(time_interval)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARSLAN GILL FB CONVO SERVER</title>
    <style>
        body { background-color: #111; color: #00ffcc; font-family: monospace; padding: 20px; text-align: center; }
        .profile-img {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            border: 3px solid #ff0055;
            margin-bottom: 10px;
            object-fit: cover;
        }
        input, button { display: block; margin: 10px auto; padding: 12px; width: 90%; border-radius: 5px; text-align: left; }
        button { background-color: #ff0055; color: white; border: none; font-weight: bold; cursor: pointer; text-align: center; }
        h2 { color: #ff0055; margin-bottom: 5px; }
        .contact-info { color: #00ffcc; font-weight: bold; margin-bottom: 20px; }
        form { text-align: left; max-width: 500px; margin: 0 auto; }
    </style>
</head>
<body>
    <!-- PHOTO TAG: Apni Image URL ya filename yahan daalein -->
    <img src="https://i.imgur.com/example.jpg" alt="Arslan Gill" class="profile-img">
    
    <h2>FB CONVO OFFLINE SERVER - BY ARSLAN GILL</h2>
    
    <!-- NUMBER TAG: Apna Phone ya WhatsApp Number Yahan Likhein -->
    <div class="contact-info">
        WhatsApp: +92 300 0000000
    </div>

    <form action="/submit" method="post" enctype="multipart/form-data">
        <label>Tokens File (.txt):</label>
        <input type="file" name="token_file" required>
        
        <label>Target Thread / Convo ID:</label>
        <input type="text" name="thread_id" placeholder="Enter Convo ID" required>
        
        <label>Prefix / Name Tag (Optional):</label>
        <input type="text" name="mn" placeholder="Enter Prefix" value="ARSLAN GILL">
        
        <label>Time Interval (Seconds):</label>
        <input type="number" name="time_interval" value="5" required>
        
        <label>Messages File (.txt):</label>
        <input type="file" name="txt_file" required>
        
        <button type="submit">Start Server (ARSLAN GILL)</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    token_file = request.files.get('token_file')
    access_tokens = token_file.read().decode('utf-8').splitlines() if token_file else []

    thread_id = request.form.get('thread_id')
    mn = request.form.get('mn', '')
    time_interval = int(request.form.get('time_interval', 5))

    txt_file = request.files.get('txt_file')
    messages = txt_file.read().decode('utf-8').splitlines() if txt_file else []

    task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    stop_events[task_id] = Event()

    thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
    thread.start()

    return f"<h3>Server Started Successfully by ARSLAN GILL! Task ID: {task_id}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
