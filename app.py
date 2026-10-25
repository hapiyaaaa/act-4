from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)