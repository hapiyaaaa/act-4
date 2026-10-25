import requests

hello_url = "https://flask-malunes-act4.onrender.com/hello"
hello_res = requests.get(hello_url)
print("Hello response:", hello_res.json())

grade_url ="https://flask-malunes-act4.onrender.com/grade?score=85"
grade_res = requests.get(grade_url)
print("Grade response", grade_res.json())