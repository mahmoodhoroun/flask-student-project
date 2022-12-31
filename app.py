import mysql.connector as mariadb
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template
import time




mariadb_connection = mariadb.connect(
    user="root", password="230799", database="ERP", host="localhost", port="3306")
create_cursor = mariadb_connection.cursor(buffered=True)

# create_cursor.execute("SELECT level_id FROM level WHERE level_name=A")

# for i in create_cursor:
#     print(i)


selected = input("Select \n1-Register New Student \n2-Enroll Course \n3-Create New Course \n4-Create Course Schedule \n5-Display Student Schedule\n")


def new_student():
    name = input("student name: ")
    birth_of_date = input("birth of date(YYYY-MM-DD): ")
    level = input("level(A, B or C): ")
    address = input("Your address: ")
    mobile_number = input("Mobile Number: ")
    email = input("Email: ")
    insert_in_contact = "INSERT INTO contact(mobile_number, email) VALUES(%s,%s);"
    data = (mobile_number, email)
    create_cursor.execute(insert_in_contact, data)
    mariadb_connection.commit()
    contact_ID = create_cursor.lastrowid
    print(contact_ID)
    level_ID = f"SELECT level_id FROM level WHERE level_name='{level}'"
    create_cursor.execute(level_ID)
    x = create_cursor.fetchall()[0][0]
    print(x)
    insert_in_address = "INSERT INTO address(address) VALUES(%s)"
    date2 = (address,)
    create_cursor.execute(insert_in_address,date2)
    mariadb_connection.commit()
    address_ID = create_cursor.lastrowid
    insert_in_student = "INSERT INTO student (student_name,contact_id,level_id,BOD,address_id) VALUES (%s, %s, %s,%s,%s)"
    data1 = (name, contact_ID, x, birth_of_date,address_ID)
    create_cursor.execute(insert_in_student, data1)
    mariadb_connection.commit()


def new_course():
    course_ID = input("Course Code (Course ID): ")
    name = input("Course name: ")
    course_level = input("Level of course(A, B or C): ")
    max_capacity = input("Max Capacity: ")
    price = input("Hour Rate (Price): ")
    level_ID = f"SELECT level_id FROM level WHERE level_name='{course_level}'"
    create_cursor.execute(level_ID)
    x = create_cursor.fetchall()[0][0]
    insert_new_course = "INSERT INTO course (course_id,level_id,course_name,max_capacity,rate_per_hour) VALUES (%s, %s, %s, %s, %s)"
    date = (course_ID, x, name, max_capacity, price)
    create_cursor.execute(insert_new_course, date)
    mariadb_connection.commit()


def enroll_course():
    student_ID = input("Student ID: ")
    course_ID = input("Course ID: ")
    total_hours = input("Total Hours: ")
    enrol_date = input("enrol_date(DD/MM/YYYY hh:mm:ss): ")
    enrol_date = datetime.strptime(enrol_date, "%d/%m/%Y %H:%M:%S")
    print(enrol_date)
    level_student = f"SELECT level_id FROM student WHERE student_id={int(student_ID)}"
    create_cursor.execute(level_student)
    x = create_cursor.fetchall()[0][0]
    print(x)
    level_course = f"SELECT level_id FROM course WHERE course_id={int(course_ID)}"
    create_cursor.execute(level_course)
    y = create_cursor.fetchall()[0][0]
    print(y, "y")
    max_capacity = f"SELECT max_capacity FROM course WHERE course_id={int(course_ID)}"
    create_cursor.execute(max_capacity)
    max_capacity_numbers = create_cursor.fetchall()[0][0]
    print(type(max_capacity_numbers), "nnnnn")
    pre_reserve = f"SELECT COUNT(course_id) FROM enrollment_history WHERE course_id={int(course_ID)}"
    create_cursor.execute(pre_reserve)
    pre_reserve_numbers = create_cursor.fetchall()[0][0]
    print(type(pre_reserve_numbers), "mmm")

    statment = f"SELECT course_id,student_id FROM enrollment_history"
    create_cursor.execute(statment)
    a = create_cursor.fetchall()
    print(a)
    rate_per_hour_statment = f"SELECT rate_per_hour FROM course WHERE course_id={int(course_ID)}"
    create_cursor.execute(rate_per_hour_statment)
    rate_per_hour = create_cursor.fetchall()[0][0]
    insert_statment = "INSERT INTO enrollment_history (student_id, course_id, enrol_date, total_hours, total) VALUES (%s, %s, %s, %s, %s);"
    data = (int(student_ID), int(course_ID), enrol_date,
            int(total_hours), int(total_hours)*rate_per_hour)
    if y == x and pre_reserve_numbers < int(max_capacity_numbers) and (course_ID, student_ID) not in a:
        print("ccccccccc")
        create_cursor.execute(insert_statment, data)
        mariadb_connection.commit()

# if level not exest 
#  else if level exest go to time step 
# check if it in the same day with any course 
# if not equal with any day add it 
# if equal check time > if (startTime > newtime < endTime) && newTime+duration =< endTime 
def convert_time_to_second(x):
    return time.mktime(datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").timetuple())

def course_schedule():
    course_id = input("Course ID: ")
    day = input("Day(Weekdays): ")
    start_time = input("Start Time(hh:mm:ss)")
    duration = input("Duration: ")
    ids_courses_statment = "SELECT course_id FROM course_schedule"
    create_cursor.execute(ids_courses_statment)
    ids_courses = create_cursor.fetchall()

    start_time = datetime.strptime(start_time, '%H:%M:%S')
    print("start_time",start_time)
    end_time_of_new_course = start_time + timedelta(hours=int(duration))
    statment1 = f"SELECT level_id FROM course WHERE course_id = {int(course_id)}"
    create_cursor.execute(statment1)
    level_of_new_course = create_cursor.fetchone()

    if course_id not in ids_courses:
        levels = []
        insert_in_course_schedule = "INSERT INTO course_schedule (course_id, start_time, duration, day) VALUES (%s, %s,%s, %s)"
        date = (int(course_id),start_time,duration,day)
        for i in ids_courses:
            statment1 = f"SELECT level_id FROM course WHERE course_id = {i[0]}"
            create_cursor.execute(statment1)
            level = create_cursor.fetchone()
            levels.append(level[0])
        if level_of_new_course[0] in levels:
            days = []
            for i in ids_courses:
                statment2 = f"SELECT day FROM course_schedule WHERE course_id = {i[0]}"
                create_cursor.execute(statment2)
                x = create_cursor.fetchone()
                days.append(x[0])
                print(days)
            if day in days:
                ids = []
                result = False
                for i in days:
                    statment3 = "SELECT course_id FROM course_schedule WHERE day=%s"
                    date2 = (i,)
                    create_cursor.execute(statment3,date2)
                    z = create_cursor.fetchone()
                    ids.append(z[0])
                for i in ids:
                    statment4 = f"SELECT start_time, duration FROM course_schedule WHERE course_id={i}"
                    create_cursor.execute(statment4)
                    y = create_cursor.fetchone()
                    start_time_of_old_course = y[0]
                    start_time_of_old_course = datetime.strptime(str(start_time_of_old_course), '%H:%M:%S')
                    
                    end_time_of_old_course = y[0] + timedelta(hours=y[1])
                    end_time_of_old_course = datetime.strptime(str(end_time_of_old_course), '%H:%M:%S')
                    if (convert_time_to_second(start_time) < convert_time_to_second(start_time_of_old_course) and convert_time_to_second(end_time_of_new_course) < convert_time_to_second(start_time_of_old_course)) or (convert_time_to_second(start_time) > convert_time_to_second(end_time_of_old_course)):
                        result = True
                if result == True:
                    create_cursor.execute(insert_in_course_schedule,date)
                    mariadb_connection.commit()
            else:
                create_cursor.execute(insert_in_course_schedule,date)
                mariadb_connection.commit()
        else:
            create_cursor.execute(insert_in_course_schedule,date)
            mariadb_connection.commit()



def student_schedule():
    student_ID = input("Student ID: ")
    course_IDs = f"SELECT course_id FROM enrollment_history WHERE student_id={int(student_ID)}"
    create_cursor.execute(course_IDs)
    ids_courses = create_cursor.fetchall()
    print(ids_courses)
    for i in ids_courses:
        courses_schedule = f"SELECT course.course_name, TIME(course_schedule.start_time), course_schedule.day FROM course JOIN course_schedule ON course.course_id=course_schedule.course_id WHERE course.course_id = {int(i[0])}"
        create_cursor.execute(courses_schedule)
        x = create_cursor.fetchall()
        print(x)



if int(selected) == 1:
    new_student()
elif int(selected) == 2:
    enroll_course()
elif int(selected) == 3:
    new_course()
elif int(selected) == 4:
    course_schedule()
elif int(selected) == 5:
    student_schedule()


