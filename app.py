from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tajny_klucz'
socketio = SocketIO(app, cors_allowed_origins="*")

shared_text = ""

@app.route('/gra-mafijna')
def gra_mafijna():
    return render_template('gra-mafijna.html')

@socketio.on('connect')
def handle_connect():
    print('Nowe połączenie')
    emit('update_text', shared_text)

@socketio.on('text_changed')
def handle_text_changed(data):
    global shared_text
    shared_text = data.get('text', '')
    if shared_text == "":
        return 
    else:
        emit('update_text', shared_text, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)