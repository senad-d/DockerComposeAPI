from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/runcmd', methods=['POST'])
def run_command():
    data = request.get_json()
    command = data.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    # Check if the command starts with 'docker-compose'
    if not command.startswith('docker-compose'):
        return jsonify({'error': 'Only docker-compose commands are allowed'}), 400

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({'output': result.decode('utf-8')}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output.decode('utf-8')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
