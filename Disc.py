from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/encender-servidor', methods=['POST'])
def encender_servidor():
    try:
        # Ejecutar el comando Java con los parámetros que utilizas
        comando = [
            'java',
            '-Xmx12G',
            '-Xms12G',
            '-jar',
            'nombre_del_archivo.jar'
        ]
        subprocess.run(comando, check=True)
        return jsonify({'mensaje': 'Servidor encendido correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al encender el servidor', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
