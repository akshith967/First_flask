from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
import json
from m1 import setup_mqtt

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ak:root@127.0.0.1:3306/company'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Employee {self.id}>'

with app.app_context():
    db.create_all()

# Set up MQTT client
mqtt_client = setup_mqtt(app, db, logger, Employees)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employees.query.all()
        employee_list = [{'id': employee.id, 'name': employee.name, 'department': employee.department} for employee in employees]
        mqtt_client.publish("display_message", "Fetched all the employees")
        return jsonify(employee_list)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch employees', 'error': str(e)}), 400

@app.route('/employees', methods=['POST'])
def create_employee():
    try:
        data = request.json
        mqtt_client.publish("display_message", "Creating a new employee")
        mqtt_client.publish("insert", json.dumps(data))
        return jsonify({'message': 'Published for creation'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to create employee', 'error': str(e)}), 400

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        mqtt_client.publish("display_message", f"Updating an employee with id {employee_id}")
        data = {
            "user": request.json,
            "e_id": employee_id
        }
        mqtt_client.publish("update", json.dumps(data))
        return jsonify({'message': 'Published for update'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update employee', 'error': str(e)}), 400

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        mqtt_client.publish("display_message", f"Deleting an employee with id {employee_id}")
        mqtt_client.publish("delete", str(employee_id))
        return jsonify({'message': 'Published for deletion'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete employee', 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=8000)
