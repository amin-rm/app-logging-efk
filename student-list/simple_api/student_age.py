from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
import logging
from fluent import handler
import json
import os

# Initialize Flask app and HTTP Basic Auth
app = Flask(__name__)
auth = HTTPBasicAuth()
app.debug = True

# Configure Fluentd handler
fluent_handler = handler.FluentHandler('flask.app', host='fluentd', port=9880)
logger = logging.getLogger('fluentd')
logger.setLevel(logging.INFO)
logger.addHandler(fluent_handler)

# Log each request to Fluentd
@app.before_request
def log_request():
    logger.info('request', {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr
    })

# Authenticate users
@auth.get_password
def get_password(username):
    if username == 'toto':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# Load student age data
try:
    student_age_file_path = os.environ['student_age_file_path']
except KeyError:
    student_age_file_path = './student_age.json'

with open(student_age_file_path, "r") as student_age_file:
    student_age = json.load(student_age_file)

# Routes
@app.route('/pozos/api/v1.0/get_student_ages', methods=['GET'])
@auth.login_required
def get_student_ages():
    return jsonify({'student_ages': student_age})

@app.route('/pozos/api/v1.0/get_student_ages/<student_name>', methods=['GET'])
@auth.login_required
def get_student_age(student_name):
    if student_name not in student_age:
        abort(404)
    age = student_age[student_name]
    del student_age[student_name]
    with open(student_age_file_path, 'w') as student_age_file:
        json.dump(student_age, student_age_file, indent=4, ensure_ascii=False)
    return jsonify({student_name: age})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Main execution
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
