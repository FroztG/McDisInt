from flask import Flask, jsonify, request
import subprocess
app = Flask(__name__)
@app.route('/disc', methods=['POST'])
def encender_servidor():
    try:
        java -Xms12G -Xmx12G -jar server.jar nogui
        return jsonify({"status": "Servidor encendido"}), 200
    subprocess.run(['java -Xms12G -Xmx12G -jar server.jar nogui']