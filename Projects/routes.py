from flask import Blueprint, request, jsonify
import json
projects_bp = Blueprint('projects_bp',__name__)


@projects_bp.route('/', methods=['GET'])
def get_projects():
    try:
        from .models import Projects
        from m1 import mqtt_client
        projects = Projects.query.all()
        project_list = [{'id': project.id, 'name': project.name, 'status': project.status} for project in projects]
        mqtt_client.publish("display_message", "Fetched all the projects")
        return jsonify(project_list)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch projects', 'error': str(e)}), 400

@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_employees(project_id):
    try:
        from .models import Projects
        from Employee.models import Employees
        from m1 import mqtt_client
        project = Projects.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        employees = Employees.query.filter_by(project_id=project_id).all()
        employee_list = [{'id': emp.id, 'name': emp.name} for emp in employees]
        data = {
            "project_id": project.id,
            "project_name":project.name,
            "project_status": project.status,
            "employees" : employee_list
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch project', 'error': str(e)}), 400

@projects_bp.route('/', methods=['POST'])
def create_employee():
    try:
        from m1 import mqtt_client
        data = request.json
        mqtt_client.publish("display_message", "Creating a new project")
        mqtt_client.publish("projects/insert", json.dumps(data))
        return jsonify({'message': 'Published for creation'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to create project', 'error': str(e)}), 400

@projects_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        from m1 import mqtt_client
        mqtt_client.publish("display_message", f"Updating an employee with id {project_id}")
        data = {
            "project": request.json,
            "p_id": project_id
        }
        mqtt_client.publish("projects/update", json.dumps(data))
        return jsonify({'message': 'Published for update'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update project', 'error': str(e)}), 400

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_employee(project_id):
    try:
        from m1 import mqtt_client
        mqtt_client.publish("display_message", f"Deleting an project with id {project_id}")
        mqtt_client.publish("projects/delete", str(project_id))
        return jsonify({'message': 'Published for deletion'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete project', 'error': str(e)}), 400
