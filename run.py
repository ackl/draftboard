#!/usr/bin/env python
from application import create_app, get_socket, get_app

app = get_app()
socket = get_socket()

if __name__ == "__main__":
    app.debug = True
    socket.run(app, host='0.0.0.0')
    #app.socketio.run(app, host='0.0.0.0')
