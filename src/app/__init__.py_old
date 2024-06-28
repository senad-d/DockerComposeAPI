from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/runcmd', methods=['POST'])
def run_command():
    command = request.json.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({'output': result.decode('utf-8')}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output.decode('utf-8')}), 500

if __name__ == '__main__':
    app.run(debug=True)
