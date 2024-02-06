from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, department, age):
        self.name = name
        self.department = department
        self.age = age

    def __repr__(self):
        return f"<Student name {self.name}>"
