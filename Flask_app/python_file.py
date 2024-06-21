
import pymysql
from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask import jsonify, request
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
    employees = Employees.query.all()
    employee_list = [{'id': employee.id, 'name': employee.name, 'department': employee.department} for employee in employees]
    return jsonify(employee_list)


@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    new_employee = Employees(name=data['name'], department=data['department'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully', 'id': new_employee.id}), 201

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employees.query.get_or_404(employee_id)
    data = request.json

    employee.name = data['name']
    employee.department = data['department']
    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employees.query.get_or_404(employee_id)

    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee deleted successfully'})
# connecting to database:

if __name__ == '__main__':
    try:
        app.run(port = 8000,debug=True)
        # db.create_all()
    except Exception as ex:
        print(ex)








