
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# ==========================================
# ACTIVITY 4: EXISTING API ENDPOINTS
# ==========================================

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


# ==========================================
# ACTIVITY 7: STUDENT DATABASE ENDPOINTS
# ==========================================

# GET ALL STUDENTS
@app.route('/students')
def get_all_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# GET ONE STUDENT BY ID
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


# FILTER STUDENTS
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


# ==========================================
# ACTIVITY 8: CRUD API ENDPOINTS
# ==========================================

# CREATE - ADD STUDENT
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No student data provided"}), 400

    required_fields = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required student fields"}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        """INSERT INTO students
        (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)""",
        (
            data['student_id'],
            data['name'],
            data['program'],
            data['year'],
            data['section']
        )
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added",
        "id": new_id
    }), 201


# READ - GET ALL STUDENTS (READ-ONLY API FOR CLASSMATES)
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()

    rows = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# READ - GET ONE STUDENT
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# UPDATE - EDIT STUDENT
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No student data provided"}), 400

    required_fields = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required student fields"}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        """UPDATE students SET
        student_id = ?,
        name = ?,
        program = ?,
        year = ?,
        section = ?
        WHERE id = ?""",
        (
            data['student_id'],
            data['name'],
            data['program'],
            data['year'],
            data['section'],
            id
        )
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated"})


# DELETE - REMOVE STUDENT
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted"})


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
