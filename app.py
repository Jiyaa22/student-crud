from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO students (AppID, Name, Email, Course, Contact)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form["appid"],
        request.form["name"],
        request.form["email"],
        request.form["course"],
        request.form["contact"]
    ))

    db.commit()
    cursor.close()
    db.close()
    return redirect("/")

@app.route("/delete/<int:appid>")
def delete(appid):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE AppID=%s",
        (appid,)
    )

    db.commit()
    cursor.close()
    db.close()
    return redirect("/")

@app.route("/edit/<int:appid>", methods=["POST"])
def edit(appid):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE students
        SET Name=%s, Email=%s, Course=%s, Contact=%s
        WHERE AppID=%s
    """, (
        request.form["name"],
        request.form["email"],
        request.form["course"],
        request.form["contact"],
        appid
    ))

    db.commit()
    cursor.close()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    app.run()