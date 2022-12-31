import mysql.connector as mariadb
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template,jsonify, g, request, redirect, url_for
import json
import requests
from functools import wraps
import time
mariadb_connection = mariadb.connect(
    user="root", password="230799", database="ERP", host="localhost", port="3306")
create_cursor = mariadb_connection.cursor()

class students_list_class:
    def __init__(self,id,name,DOB,mobile_number,email,level,address):
        self.id = id 
        self.name =name
        self.DOB = DOB
        self.mobile_number = mobile_number
        self.email = email
        self.level = level
        self.address = address
        
API_KEY = "abc123"

def auth_validation(token, API_KEY):
    if token is None:
        return False
    if token == API_KEY:
        return True

def students_list():
    IDs = "SELECT student_id FROM student"
    create_cursor.execute(IDs)
    student_ids= create_cursor.fetchall()
    result = []
    for i in student_ids:
        statment1 = f"SELECT student_name FROM student WHERE student_id={i[0]}"
        create_cursor.execute(statment1)
        student_name = create_cursor.fetchone()
        statment2 = f"SELECT BOD FROM student WHERE student_id={i[0]}"
        create_cursor.execute(statment2)
        date_of_birth= create_cursor.fetchone()
        statment3 = f"SELECT contact.mobile_number, contact.email FROM contact JOIN student ON contact.contact_id = student.contact_id WHERE student.student_id={i[0]}"
        create_cursor.execute(statment3)
        contact= create_cursor.fetchone()
        mobile_number = contact[0]
        email = contact[1]
        statment4 = f"SELECT level.level_name FROM level JOIN student ON level.level_id = student.level_id WHERE student.student_id={i[0]}"
        create_cursor.execute(statment4)
        level = create_cursor.fetchone()
        statment5 = f"SELECT address.address FROM address JOIN student ON address.address_id = student.address_id WHERE student.student_id={i[0]}"
        create_cursor.execute(statment5)
        address = create_cursor.fetchone()
        result.append(students_list_class(i[0],student_name[0],date_of_birth[0],mobile_number,email,level[0],address[0]))
    return result


class courses_list_class:
    def __init__(self,id,name,level,max_capacity,rate_per_hour):
        self.id = id 
        self.name =name
        self.level = level
        self.max_capacity = max_capacity
        self.rate_per_hour = rate_per_hour



def courses_list():
    IDs = "SELECT course_id FROM course"
    create_cursor.execute(IDs)
    courses_ids= create_cursor.fetchall()
    result2 = []
    for i in courses_ids:
        statment1 = f"SELECT course_name,max_capacity,rate_per_hour FROM course WHERE course_id = {i[0]}"
        create_cursor.execute(statment1)
        elements = create_cursor.fetchall()
        statment2 = f"SELECT level.level_name FROM level JOIN course ON level.level_id = course.level_id WHERE course.course_id = {i[0]}"
        create_cursor.execute(statment2)
        level = create_cursor.fetchone()
        print(level[0])
        print(elements[0])
        result2.append(courses_list_class(i[0],elements[0][0],level[0],elements[0][1],elements[0][2]))
    return result2


class courses_schedules_class:
    def __init__(self,id,name,level,day,start_time,duration):
        self.id = id 
        self.name =name
        self.level = level
        self.day = day
        self.start_time = start_time
        self.duration = duration


def courses_schedules():
    ids = "SELECT course_id FROM course_schedule"
    create_cursor.execute(ids)
    courses_ids = create_cursor.fetchall()
    result3 = []
    for i in courses_ids:
        statment1 = f"SELECT course_name FROM course WHERE course_id={i[0]}"
        create_cursor.execute(statment1)
        course_name = create_cursor.fetchone()
        statment2 = f"SELECT level.level_name FROM level JOIN course ON level.level_id = course.level_id WHERE course.course_id={i[0]}"
        create_cursor.execute(statment2)
        level = create_cursor.fetchone()
        statment3 = f"SELECT day, start_time, duration FROM course_schedule WHERE course_id={i[0]}"
        create_cursor.execute(statment3)
        elements = create_cursor.fetchone()
        result3.append(courses_schedules_class(i[0],course_name[0],level[0],elements[0],elements[1],elements[2]))
        print("course id:",i[0],"course name:",course_name[0],"level:",level[0],"day:",elements[0],"start_time",elements[1],"duration:",elements[2])
    return result3

# print(courses_schedules())
# courses_schedules()
student_details_json = "SELECT * FROM student"
create_cursor.execute(student_details_json)
x = create_cursor.fetchall()
# # x = dict(x)
# x = dict((y) for y in x)


app = Flask(__name__)
@app.route("/")
def home():
    return render_template("/template.html")


@app.route("/students_list.html")
def students_list_view():
    result = students_list()
    return render_template("/students_list.html", result=result)

@app.route("/courses_list.html")
def courses_list_view():
    result = courses_list()
    return render_template("/courses_list.html", result=result)

@app.route("/courses_schedules.html")
def courses_schedules_list_view():
    result = courses_schedules()
    return render_template("/courses_schedules.html", result=result)




@app.route("/student_details", methods=['GET'] )
def student_details():
    token = request.args.get('token')
    print(token)
    print(API_KEY)
    print(API_KEY == token)
    print(x)

    if auth_validation(token, API_KEY):
        return  jsonify(x)
    return {'error':"Enter valid api key"}



@app.route("/student_details/<int:student_id>", methods=['GET'])
def student_details_id(student_id):
    token = request.args.get('token')
    if auth_validation(token, API_KEY):
        return jsonify(x[student_id])
    return {'error':"Enter valid api key"}



app.run(debug=True)