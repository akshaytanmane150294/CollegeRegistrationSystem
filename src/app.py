from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'secret_key'

# Establish a global MySQL connection


def get_db_connection():
    return pymysql.connect(
        host='DESKTOP-QAKELSA\SQLEXPRESS',
        user='DESKTOP-QAKELSA\\aksha',
        password='Art@150294@',
        database='CollegeRegistrationSystem',
        # cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/')
def index():
    return redirect(url_for('manage_dashboard'))


@app.route('/dashboard')
def manage_dashboard():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Fetch students with department names
        cursor.execute("""
            SELECT s.StudentID, s.Name, s.Email, d.DepartmentName
            FROM Student s
            LEFT JOIN Department d ON s.DepartmentID = d.DepartmentID
        """)
        students = cursor.fetchall()

        # Fetch registrations with related student and course info
        cursor.execute("""
            SELECT r.RegistrationID, s.Name AS StudentName, c.CourseName, r.Status, r.RegistrationDate, r.Semester
            FROM Registration r
            JOIN Student s ON r.StudentID = s.StudentID
            JOIN Course c ON r.CourseID = c.CourseID
        """)
        registrations = cursor.fetchall()
    connection.close()
    return render_template('manage_dashboard.html', students=students, registrations=registrations)


@app.route('/edit/student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Fetch the student record
        cursor.execute(
            "SELECT * FROM Student WHERE StudentID = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            flash('Student not found!', 'danger')
            return redirect(url_for('manage_dashboard'))

        # Fetch departments for dropdown
        cursor.execute("SELECT * FROM Department")
        departments = cursor.fetchall()

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            department_id = request.form['department']
            # Update student record
            cursor.execute("""
                UPDATE Student 
                SET Name = %s, Email = %s, DepartmentID = %s 
                WHERE StudentID = %s
            """, (name, email, department_id, student_id))
            connection.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('manage_dashboard'))
    connection.close()
    return render_template('edit_student.html', student=student, departments=departments)


@app.route('/delete/student/<int:student_id>')
def delete_student(student_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Delete student record
        cursor.execute(
            "DELETE FROM Student WHERE StudentID = %s", (student_id,))
        connection.commit()
    connection.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('manage_dashboard'))


@app.route('/edit/registration/<int:registration_id>', methods=['GET', 'POST'])
def edit_registration(registration_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Fetch the registration record
        cursor.execute(
            "SELECT * FROM Registration WHERE RegistrationID = %s", (registration_id,))
        registration = cursor.fetchone()
        if not registration:
            flash('Registration not found!', 'danger')
            return redirect(url_for('manage_dashboard'))

        # Fetch students and courses for dropdowns
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()
        cursor.execute("SELECT * FROM Course")
        courses = cursor.fetchall()

        if request.method == 'POST':
            student_id = request.form['student']
            course_id = request.form['course']
            status = request.form['status']
            registration_date = request.form['date']
            semester = request.form['semester']
            # Update registration record
            cursor.execute("""
                UPDATE Registration 
                SET StudentID = %s, CourseID = %s, Status = %s, RegistrationDate = %s, Semester = %s
                WHERE RegistrationID = %s
            """, (student_id, course_id, status, registration_date, semester, registration_id))
            connection.commit()
            flash('Registration updated successfully!', 'success')
            return redirect(url_for('manage_dashboard'))
    connection.close()
    return render_template('edit_registration.html', registration=registration, students=students, courses=courses)


@app.route('/delete/registration/<int:registration_id>')
def delete_registration(registration_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Delete registration record
        cursor.execute(
            "DELETE FROM Registration WHERE RegistrationID = %s", (registration_id,))
        connection.commit()
    connection.close()
    flash('Registration deleted successfully!', 'success')
    return redirect(url_for('manage_dashboard'))


if __name__ == '__main__':
    app.run()
