from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import subprocess
import shlex
import os
import logging

app = Flask(__name__)

log_dir = '/app'
log_file = os.path.join(log_dir, 'api.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('MY_JWT_SECRET_KEY', 'your_default_jwt_secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False 
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    logger.debug('Login attempt')
    if not request.is_json:
        logger.warning('Missing JSON in request')
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    env_username = os.getenv('API_USERNAME', 'admin')
    env_password = os.getenv('API_PASSWORD', 'password')

    if username != env_username or password != env_password:
        logger.warning('Bad username or password')
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    logger.info('Login successful')
    return jsonify(access_token=access_token), 200

@app.route('/runcmd', methods=['POST', 'OPTIONS'])
@jwt_required()
def run_command():
    logger.debug('Run command request')
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    command = data.get('command')

    if not command:
        logger.error('No command provided')
        return jsonify({'error': 'No command provided'}), 400

    if not command.startswith('docker-compose'):
        logger.error('Invalid command: %s', command)
        return jsonify({'error': 'Only docker-compose commands are allowed'}), 400

    try:
        logger.info('Executing command: %s', command)
        command_list = shlex.split(command)
        result = subprocess.check_output(command_list, stderr=subprocess.STDOUT)
        logger.info('Command executed successfully')
        return jsonify({'output': result.decode('utf-8')}), 200
    except subprocess.CalledProcessError as e:
        logger.error('Command execution failed: %s', e.output.decode('utf-8'))
        return jsonify({'error': e.output.decode('utf-8')}), 500
    except Exception as e:
        logger.exception('Unexpected error occurred')
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_security_headers(response):
    logger.debug('Adding security headers')
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(400)
def handle_400_error(e):
    logger.error('400 error: %s', str(e))
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(401)
def handle_401_error(e):
    logger.error('401 error: %s', str(e))
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(404)
def handle_404_error(e):
    logger.error('404 error: %s', str(e))
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def handle_500_error(e):
    logger.error('500 error: %s', str(e))
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
