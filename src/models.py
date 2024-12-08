from app import db

class Department(db.Model):
    __tablename__ = 'Department'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)

class Student(db.Model):
    __tablename__ = 'Student'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('Department.department_id'))

class Course(db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer)

class Registration(db.Model):
    __tablename__ = 'Registration'
    registration_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    status = db.Column(db.Enum('Registered', 'Dropped', 'Completed'), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    semester = db.Column(db.String(50), nullable=False)
