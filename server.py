from flask import Flask, request
from flask_socketio import SocketIO
from planner import update_user_activity
from mistral import ask_mistral

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []

@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)

def send_to_clients(message):
    for client in clients:
        socketio.emit("message", message, room=client)

context_memory = []

def get_context():
    return context_memory[-10:]

@app.route("/message", methods=["POST"])
def receive_message():
    data = request.json
    text = data.get("text")

    update_user_activity()

    context_memory.append({"user": text})

    response = ask_mistral(context_memory)

    context_memory.append({"assistant": response})

    send_to_clients(response)

    return {"response": response}

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
