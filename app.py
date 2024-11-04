from flask import Flask, render_template, url_for, request
import sqlite3 as sql

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to display the form to add a new student
@app.route('/enternew')
def new_student():
    return render_template('student.html')

# Route to add a new record to the database
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            passw = request.form['passw']

            # Connect to the database and insert the new record
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (name, passw) VALUES (?, ?)", (name, passw))
                con.commit()
                msg = "Record successfully added"
        except:
            # Rollback in case of error
            con.rollback()
            msg = "Error in insert operation"
        finally:
            # Render the result page with the message
            return render_template("result.html", msg=msg)
            con.close()

# Route to list all records in the database
@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return render_template('list.html', rows=rows)

# Route to handle user login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            passw = request.form['passw']
            print(name, request)

            # Connect to the database and check if the user exists
            with sql.connect("database.db") as con:
                cur = con.cursor()
                try:
                    sqlite_insert_query = """SELECT * FROM users WHERE
                    name='""" + name + """' AND passw='""" + passw + """'"""
                    cur.execute(sqlite_insert_query)
                    records = cur.fetchall()
                    if len(records) >= 1:
                        msg = "Bingo" + " " 
                    else:
                        msg = "Nope"
                except:
                    msg = "Nope2"
        except:
            msg = "Error in insert operation" + " " + msg
        finally:
            # Render the result page with the message
            return render_template("result.html", msg=msg)
            con.close()

if __name__ == "__main__":
    app.run(debug=True)
