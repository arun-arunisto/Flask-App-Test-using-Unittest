import unittest
from main import app, db, Student


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' #using an in-memory database for testing
        with app.app_context():
            db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    #home page testing
    def test_home_route(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Home page test failed")

    #test for adding student
    def test_add_student_success(self):
        response = self.app.post('/add_student', data=dict(
            stu_name='Test Name',
            stu_dept='Test Department',
            stu_age='25'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200, 'Add student test code failed')
        self.assertIn(b'Added Successfully', response.data, 'Flash message failed')

        #checking that data inserted successfully!!
        with app.app_context():
            student = Student.query.filter_by(name='Test Name').first()
            self.assertIsNotNone(student, 'student not added!')
            self.assertEqual(student.department, 'Test Department', 'department not added')
            self.assertEqual(student.age, 25, 'age not added')

    # test for retrieve data from student table
    def test_student_list_route(self):
        with app.app_context():
            # creating and adding data
            stu_1 = Student(name='Arun Arunisto', department='Computer Science', age=25)
            stu_2 = Student(name='Gokul Che', department='Commerce', age=20)
            db.session.add_all([stu_1, stu_2])
            db.session.commit()

            response = self.app.get('/student_list', follow_redirects=True)

        self.assertEqual(response.status_code, 200, "student list route test failed")
        self.assertIn(b'Arun Arunisto', response.data, 'Student data not found in response')

    #test for deleting data
    def test_delete_student_route(self):
        with app.app_context():
            #creating students
            student = Student(name="Arun Arunisto", department="Computer Science", age=25)
            db.session.add(student)
            db.session.commit()

            #getting students id from the database
            student_id = student.id

            #confirm that the data in the database
            self.assertIsNotNone(Student.query.get(student_id), 'Student not found before delete')

            #make a request to delete the student
            response = self.app.post(f'/delete_student/{student_id}', follow_redirects=True)

            #confirm the student is no longer present in the database after deletion
            self.assertIsNone(Student.query.get(student_id), 'Student not deleted')

        #check if the response redirects to the student_list route
        self.assertEqual(response.status_code, 200, 'Delete student route test failed')

    #testing add student failure with empty name
    def test_add_student_failure_empty_name(self):
        response = self.app.post('/add_student', data=dict(
            stu_name='',
            stu_dept='Test Department',
            stu_age='25'
        ), follow_redirects=True)

        #print(response.data)
        self.assertEqual(response.status_code, 400, 'Data added failure test case failed')
        self.assertIn(b'400 Bad Request', response.data, '400 bad request test failed!')

        #checking that data is not inserted
        with app.app_context():
            students = Student.query.all()
            self.assertEqual(len(students), 0, 'Data failure test failed')

if __name__ == "__main__":
    unittest.main()