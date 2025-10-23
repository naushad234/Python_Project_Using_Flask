from flask import Flask, redirect, render_template, request

from db import get_connection

app = Flask(__name__)
def calculate_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        sub1 = float(request.form['sub1'])
        sub2 = float(request.form['sub2'])
        sub3 = float(request.form['sub3'])
        sub4 = float(request.form['sub4'])
        sub5 = float(request.form['sub5'])

        total = sub1 + sub2 + sub3 + sub4 + sub5
        percentage = total / 5
        grade = calculate_grade(percentage)
        result = "Pass" if percentage >= 40 else "Fail"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO grades(student_name, sub1, sub2, sub3, sub4, sub5, total, percentage, grade, result)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (name, sub1, sub2, sub3, sub4, sub5, total, percentage, grade, result))
        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("index.html")

@app.route("/view")
def view():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grades")
    data = cursor.fetchall()
    conn.close()
    return render_template("view.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
