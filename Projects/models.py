from db import db
class Projects(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    status = db.Column(db.Boolean, default = False)
    employees = db.relationship('Employees', backref='projects')

    def __repr__(self):
        return f'<Project {self.id}>'