from flask import Flask
import logging
from flask_migrate import Migrate
from db import db

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


app = Flask(__name__)

from Employee.routes import employees_bp
from Projects.routes import projects_bp

app.register_blueprint(employees_bp, url_prefix='/employees')
app.register_blueprint(projects_bp, url_prefix='/projects')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ak:root@127.0.0.1:3306/company'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate()
migrate.init_app(app, db)
db.init_app(app)
from Employee.models import Employees
from Projects.models import Projects
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World',200

if __name__ == '__main__':
    app.run()






