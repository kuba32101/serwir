from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)

pokoje = []

app.config['SECRET_KEY'] = 'q9eryvcnjisnsxuc'
socketio = SocketIO(app, cors_allowed_origins="*")
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gra-mafijna-lobby')
def gra_mafijna():
    return render_template('gra-mafijna-lobby.html')

@socketio.on('connect')
def handle_connect():
    print("Nowe połączenie")
    emit('connectRom', pokoje)
    
@socketio.on('robPokoj')
def robPokoj(data):
    global pokoje
    if data in pokoje:
        emit('pokujNE')
        return
    else:
        pokoje.append(data)
        emit('pokujOK', data, broadcast=True)
        print("new pokuj")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)