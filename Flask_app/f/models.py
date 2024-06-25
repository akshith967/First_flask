from . import db

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<Employee {self.id}>'

class Audits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<audit {self.id}>'

