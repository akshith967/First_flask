import json

def insert_table(client, userdata, message):
    from app import app, db, logger
    from .models import Projects
    try:
        with app.app_context():
            data = json.loads(message.payload.decode())
            new_project = Projects(name=data['name'], status = data.get('status'))
            db.session.add(new_project)
            db.session.commit()
            client.publish("display_message", f"Project created successfully with id: {new_project.id}")
    except Exception as e:
        client.publish("display_message", "Creation of Project failed")
        logger.error(f"Failed to create Project: {e}")

def update_table(client, userdata, message):
    from app import app, db, logger
    from .models import Projects
    try:
        with app.app_context():
            data = json.loads(message.payload.decode())
            project = Projects.query.get_or_404(data['p_id'])
            if data['project'].get('name') != None:
                project.name = data['project'].get('name')
            if data['project'].get('status') != None:
                project.status = data['project'].get('status')
            db.session.commit()
            client.publish("display_message", f"Project updated successfully with id: {data['p_id']}")
    except Exception as e:
        client.publish("display_message", f"Updation of project failed with id: {data['p_id']}")
        logger.error(f"Failed to update employee: {e}")

def delete_record(client, userdata, message):
    from app import app, db, logger
    from .models import Projects
    try:
        with app.app_context():
            project_id = int(message.payload.decode())
            project = Projects.query.get_or_404(project_id)
            db.session.delete(project)
            db.session.commit()
            client.publish("display_message", f"Employee deleted successfully with id: {project_id}")
    except Exception as e:
        client.publish("display_message", f"Deletion of project failed with id: {project_id}")
        logger.error(f"Failed to delete project: {e}")
