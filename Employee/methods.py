import json

def insert_table(client, userdata, message):
    from app import app, db, logger
    from .models import Employees
    try:
        with app.app_context():
            data = json.loads(message.payload.decode())
            new_employee = Employees(name=data['name'], department=data['department'])
            db.session.add(new_employee)
            db.session.commit()
            client.publish("display_message", f"Employee created successfully with id: {new_employee.id}")
    except Exception as e:
        client.publish("display_message", "Creation of employee failed")
        logger.error(f"Failed to create employee: {e}")

def update_table(client, userdata, message):
    from app import app, db, logger
    from Employee.models import Employees
    try:
        with app.app_context():
            data = json.loads(message.payload.decode())
            employee = Employees.query.get_or_404(data['e_id'])
            if(data['user'].get('name') != None):
                employee.name = data['user'].get('name')
            if (data['user'].get('department') != None):
                employee.department = data['user'].get('department')
            if(data['user'].get('experience') != None):
                employee.experience = data['user'].get('experience')
            if(data['user'].get('project_id') != None):
                employee.project_id = data['user'].get('project_id')
            db.session.commit()
            client.publish("display_message", f"Employee updated successfully with id: {data['e_id']}")
    except Exception as e:
        client.publish("display_message", f"Updation of employee failed with id: {data['e_id']}")
        logger.error(f"Failed to update employee: {e}")

def delete_record(client, userdata, message):
    from app import app, db, logger
    from Employee.models import Employees
    try:
        with app.app_context():
            employee_id = int(message.payload.decode())
            employee = Employees.query.get_or_404(employee_id)
            db.session.delete(employee)
            db.session.commit()
            client.publish("display_message", f"Employee deleted successfully with id: {employee_id}")
    except Exception as e:
        client.publish("display_message", f"Deletion of employee failed with id: {employee_id}")
        logger.error(f"Failed to delete employee: {e}")
