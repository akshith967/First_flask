from flask import Blueprint, request, jsonify
import json
employees_bp = Blueprint('employees_bp',__name__)


@employees_bp.route('/', methods=['GET'])
def get_employees():
    try:
        from Employee.models import Employees
        from m1 import mqtt_client
        employees = Employees.query.all()
        employee_list = [{'id': employee.id, 'name': employee.name, 'department': employee.department} for employee in employees]
        mqtt_client.publish("display_message", "Fetched all the employees")
        return jsonify(employee_list)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch employees', 'error': str(e)}), 400

@employees_bp.route('/', methods=['POST'])
def create_employee():
    try:
        from m1 import mqtt_client
        data = request.json
        mqtt_client.publish("display_message", "Creating a new employee")
        mqtt_client.publish("employee/insert", json.dumps(data))
        return jsonify({'message': 'Published for creation'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to create employee', 'error': str(e)}), 400

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        from m1 import mqtt_client
        mqtt_client.publish("display_message", f"Updating an employee with id {employee_id}")
        data = {
            "user": request.json,
            "e_id": employee_id
        }
        mqtt_client.publish("employee/update", json.dumps(data))
        return jsonify({'message': 'Published for update'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update employee', 'error': str(e)}), 400

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        from m1 import mqtt_client
        mqtt_client.publish("display_message", f"Deleting an employee with id {employee_id}")
        mqtt_client.publish("employee/delete", str(employee_id))
        return jsonify({'message': 'Published for deletion'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete employee', 'error': str(e)}), 400

#  Assigning project_id to the employee
