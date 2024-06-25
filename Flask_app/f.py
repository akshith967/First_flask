
import pymysql
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask import jsonify, request
import paho.mqtt.client as mqtt
# Mqtt code
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"T1")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
def on_publish(client, userdata, mid):
    print(f"Message published! by {client._client_id.decode()}")


app = Flask(__name__)

user = 'ak'
password = 'root'
host = '127.0.0.1'
port = 3306
database = 'company'

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<Employee {self.id}>'

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employees.query.all()
        employee_list = [{'id': employee.id, 'name': employee.name, 'department': employee.department} for employee in employees]
        client.publish("audit_request","fetched all the employees")
        return jsonify(employee_list)
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/employees', methods=['POST'])
def create_employee():
    try:
        data = request.json
        new_employee = Employees(name=data['name'], department=data['department'])
        db.session.add(new_employee)
        db.session.commit()
        client.publish("audit_request", f"Employee created successfully with id: {new_employee.id}")
        return jsonify({'message': 'Employee created successfully', 'id': new_employee.id}), 201
    except Exception as e:
        client.publish("audit_request", "Failed to add employee due to bad format/lack of data")
        return jsonify({'message': 'Failed to create employee', 'error': str(e)}), 400
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        employee = Employees.query.get_or_404(employee_id)
        data = request.json
        employee.name = data['name']
        employee.department = data['department']
        db.session.commit()
        client.publish("audit_request", f"Employee with id: {employee.id} updated successfully")
        return jsonify({'message': 'Employee updated successfully'})
    except Exception as e:
        db.session.rollback()
        client.publish("audit_request", f"Failed to update employee with id: {employee_id} due to bad format/lack of data")
        return jsonify({'message': 'Failed to update employee', 'error': str(e)}), 400

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = Employees.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        client.publish("audit_request", f"Employee with id: {employee.id} deleted successfully")
        return jsonify({'message': 'Employee deleted successfully'})
    
    except Exception as e:
        client.publish("audit_request", f"Failed to delete employee with id: {employee_id}")
        return jsonify({'message': 'Failed to delete employee', 'error': str(e)}), 400


if __name__ == '__main__':
    try:
        app.run(port = 8000,debug=True)
        
    except Exception as ex:
        print(ex)








