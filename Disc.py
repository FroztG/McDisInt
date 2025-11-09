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
        subprocess.Popen(comando, check=True)
        return jsonify({'mensaje': 'Servidor encendido correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al encender el servidor', 'error': str(e)}), 500

@app.route('/apagar-servidor', methods=['POST'])
def apagar_servidor():
    subprocess.run(['pkill', '-f', 'nombre_del_archivo.jar'], check=False)
    return jsonify({'mensaje': 'Servidor apagado correctamente'}), 200

@app.route('/reiniciar-servidor', methods=['POST'])
def reiniciar_servidor():
    """
    Primero apaga el servidor y luego lo vuelve a iniciar.
    """
    try:
        # 1. Apagar el servidor
        subprocess.run(['pkill', '-f', JAR_FILE], check=False)
        
        # Damos un segundo para que el proceso muera completamente
        time.sleep(1) 
        
        # 2. Encender el servidor
        # Usamos Popen de nuevo para iniciarlo en segundo plano.
        subprocess.Popen(JAVA_COMMAND)
        
        return jsonify({'mensaje': 'Servidor reiniciado correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al reiniciar el servidor', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
