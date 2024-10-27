from flask import Flask, render_template, request, redirect, url_for
import qrcode
import openpyxl
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    roll_number = db.Column(db.String(50))
    score = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    questions = [
        {"id": 1, "question": "What is 2 + 2?", "options": ["2", "3", "4", "5"], "answer": "4"},
    ]
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit_quiz():
    name = request.form['name']
    email = request.form['email']
    roll_number = request.form['roll_number']
    score = 0  # Logic to calculate score from submitted answers

    new_student = Student(name=name, email=email, roll_number=roll_number, score=score)
    db.session.add(new_student)
    db.session.commit()

    file_path = 'results.xlsx'
    if not os.path.exists(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Name", "Email", "Roll Number", "Score"])
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

    sheet.append([name, email, roll_number, score])
    workbook.save(file_path)

    return redirect(url_for('result', score=score))

@app.route('/result/<int:score>')
def result(score):
    return render_template('result.html', score=score)

@app.route('/generate_qr')
def generate_qr():
    qr_data = url_for('quiz', _external=True)
    qr_img = qrcode.make(qr_data)
    qr_img.save('static/qrcodes/quiz_qr.png')
    return "QR code generated!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
