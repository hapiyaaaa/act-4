
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# EXISTING ACTIVITY 4 ENDPOINTS

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00143",
        "name": "HApee Malunes",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


@app.route('/grade')
def get_grade():
    score = float(request.args.get('score', 0))

    if score >= 75:
        remark = "Very Good"
    else:
        remark = "Needs Improvement"

    return jsonify({
        "score": score,
        "remark": remark
    })


# ACTIVITY 7: GET ALL STUDENTS
@app.route('/students')
def get_all_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ACTIVITY 7: GET ONE STUDENT BY ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ADDITIONAL TASK: FILTER STUDENTS
@app.route('/students/filter')
def filter_students():

    program = request.args.get('program')
    year = request.args.get('year')
    section = request.args.get('section')

    filters = []
    values = []

    if program:
        filters.append("program = ?")
        values.append(program)

    if year:
        filters.append("year = ?")
        values.append(year)

    if section:
        filters.append("section = ?")
        values.append(section)

    if not filters:
        return jsonify({
            "error": "Please provide program, year, or section."
        }), 400

    query = "SELECT * FROM students WHERE " + " AND ".join(filters)

    conn = get_db_connection()

    students = conn.execute(query, values).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
