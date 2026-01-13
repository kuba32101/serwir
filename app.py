from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tajny_klucz'
socketio = SocketIO(app, cors_allowed_origins="*")

shared_text = ""

@app.route('/')
def gra_mafijna():
    return render_template('index.html')
    
@socketio.on('connect')
def handle_connect():
    print('Nowe połączenie')

@socketio.on('update_text')
def update_history(data):
    inp = data.get('inp')
    text = data.get('text')
    if not inp or not text:
        return
    
    emit('update_history', {'inp': inp, 'text': text}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)