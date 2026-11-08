
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year TEXT NOT NULL,
    section TEXT NOT NULL
)
""")

# Delete old student records
cursor.execute("DELETE FROM students")

# Insert 5 BSIT 3rd Year student records
students = [
    ("2026-0001", "Sharmaine Joyce Palencia", "BSIT", "3", "B"),
    ("2026-0002", "Jero Paca-oncis", "BSIT", "3", "B"),
    ("2026-0003", "Missy Miranda", "BSIT", "3", "B"),
    ("2026-0004", "Ana Garcia", "BSIT", "3", "A"),
    ("2026-0005", "Mark Lopez", "BSIT", "3", "A")
]

# Insert records into the students table
cursor.executemany("""
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

# Save database changes
conn.commit()

# Close database connection
conn.close()

# Display success message
print("Database initialized successfully!")
print("5 BSIT 3rd Year student records inserted.")
