from flask import Flask, render_template, redirect, url_for, request, flash, abort
from models import db, Student
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wqqeqweqwe'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/add_student", methods=["POST", "GET"])
def add_student():
    if request.method == 'POST':
        name = request.form['stu_name']
        dept = request.form['stu_dept']
        age = request.form['stu_age']
        if name:
            try:
                student = Student(name, dept, age)
                db.session.add(student)
                db.session.commit()
                flash('Added Successfully', 'success')
            except Exception as e:
                flash('Something went wrong!!',"failed")
        else:
            abort(400) # return a 400 bad request status code if name is empty
    return redirect(url_for('home'))

@app.route("/student_list")
def student_list():
    student = Student.query.all()
    print(student)
    return render_template('student_list.html', data=[{'student':student}])

@app.route("/delete_student/<int:id>", methods=["GET", "POST"])
def delete_student(id):
    print(id)
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('student_list'))

if __name__ == '__main__':
    app.run(debug=True)