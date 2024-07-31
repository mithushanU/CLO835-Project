from flask import Flask, render_template, request
from pymysql import connections
import os

app = Flask(__name__)

# Retrieve environment variables for database connection
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))
GROUP_NAME = os.environ.get("GROUP_NAME", "Default Group")
BACKGROUND_URL = os.environ.get("IMAGE", "failed to load")

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', GROUP_NAME=GROUP_NAME, background=BACKGROUND_URL)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', GROUP_NAME=GROUP_NAME, background=BACKGROUND_URL)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    except Exception as e:
        print(f"Error: {e}")
        emp_name = "Error adding employee"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", GROUP_NAME=GROUP_NAME, background=BACKGROUND_URL)

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    emp_id = request.form['emp_id']
    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            output["emp_id"] = "Not Found"
            output["first_name"] = "Not Found"
            output["last_name"] = "Not Found"
            output["primary_skills"] = "Not Found"
            output["location"] = "Not Found"
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], GROUP_NAME=GROUP_NAME, background=BACKGROUND_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
