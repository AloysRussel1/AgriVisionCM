from app import create_app, socketio

# Crée l'application Flask
app = create_app()

# Lance le serveur Flask avec SocketIO pour gérer les événements en temps réel
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)