from datetime import date, datetime
from flask import Flask, request, sessions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import mode
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import models
from database import SessionLocal, engine
import os

"""
Functions:

1. .intro - about the bot && user. [DONE]
2. .pday / .pending - Work left for today. [DONE]
3. .add {task} Optional[DD/MM/YYYY] - adds task in the above format. [DONE]
4. .done {task} Optional[DD/MM/YYYY] - Should be sth left today && should be in the list else given an error message. [DONE]
5. .pmonth - Work left for the month. [DONE]
6. .aday / .done - Work done today. [DONE]
7. .amonth - Work done this month. [DONE
8. .help - informs about the available options [DONE]

Can add on more to see sth like stats. will come back later to this.
"""

"""
Ideas:

Split this file to utils.py
"""

intro = """
Welcome To Keep Me On Track Bot.
The bot is built using twilio and flask, it's deployed on heroku.
To know more about the available features enter '.help'.
"""

help = """
1. .intro - about the bot && user.
2. .pday / .pending - Work left for today.
3. .add [task] optional[DD/MM/YYYY] - adds task in the above format.
4. .done [task] optional[DD/MM/YYYY]- Should be sth left && should be in the list else given an error message.
5. .pmonth - Work left for the month.
6. .aday / .done - Work done today.
7. .amonth - Work done this month.
8. .help - informs about the available options
"""

default_msg = "Woops idk what that means!! Sorreyy!!!\nTry '.help' to understand me better *insert puppy face*."

def add_task(task):

    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)

    # Default Date For the Task
    date = datetime.datetime.today().strftime('%d/%m/%y')
    if task[-1]==']':
        date = task[-9:-1]
        task = task[0:-11]

    db_task = models.Task(
        date=date,
        task=task,
        status="Pending"
    )

    print (db_task)
    db.add(db_task)
    db.commit()
    db.close()

    return "Task Added Successfully!!"

def get_task():

    db = SessionLocal()

    todays_date = datetime.datetime.today().strftime('%d/%m/%y')
    taskList = db.query(models.Task).filter_by(date=todays_date, status="Pending").all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Woahhh!! Nothing pending Today.\n*YOU ARE ON TRACKK*"

    tasks = ""
    for task in taskList:
        tasks+= task.task +" from date "+task.date+"\n"

    return tasks

def get_months_task():
    db = SessionLocal()

    month = "___"+datetime.datetime.today().strftime('%m')+"%"
    taskList = db.query(models.Task).filter_by(status="Pending").filter(models.Task.date.like(month)).all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Woahhh!! Nothing pending this month.\n*YOU ARE ON TRACKK*"

    tasks = ""
    for task in taskList:
        tasks+= task.task +" from date "+task.date+"\n"

    return tasks


def mark_done(task):
    db = SessionLocal()
    date = datetime.datetime.today().strftime('%d/%m/%y')
    
    if task[-1]==']':
        date = task[-9:-1]
        task = task[0:-11]

    mark_task = db.query(models.Task).filter_by(task=task, date=date, status="Pending")

    print(mark_task)
    if mark_task == None:
        db.close()
        return "Oopsie task not found"
    
    mark_task.update({models.Task.status:"Done"},synchronize_session = False)
    
    db.commit()
    db.close()
    return "Task Mark Done successfully!!"

def get_done():

    db = SessionLocal()

    todays_date = datetime.datetime.today().strftime('%d/%m/%y')
    taskList = db.query(models.Task).filter_by(date=todays_date, status="Done").all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Get workin pal, dont't be lazy.\n*Screamss*"

    tasks = "Work done today.\n"
    for task in taskList:
        tasks+= task.task +" from date "+task.date+"\n"

    tasks += "Good Going."
    return tasks

def get_done_month():
    db = SessionLocal()

    month = "___"+datetime.datetime.today().strftime('%m')+"%"
    taskList = db.query(models.Task).filter_by(status="Done").filter(models.Task.date.like(month)).all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Woahhh!! No accomplishment for the months.\n*Screamsss*"

    tasks = "Work Done this month.\n"
    for task in taskList:
        tasks+= task.task +" from date "+task.date+"\n"

    return tasks


def get_response(msg):
    if msg == ".intro":
        return intro
    elif msg == ".help":
        return help
    elif msg[0:4] == ".add":
        return add_task(msg[5:])
    elif msg[0:5] == ".pday" or msg[0:9]==".pending":
        return get_task()
    elif msg[0:7] == ".pmonth":
        return get_months_task()
    elif msg[0:5] == ".done":
        return mark_done(msg[6:])
    elif msg[0:] == ".aday":
        return get_done()
    elif msg[0:] == ".amonth":
        return get_done_month()
    return default_msg

"""
# Uncomment below code while testing.
print (get_response(".add Task1"))
print (get_response(".add Adding date [23/11/21]"))
print (get_response(".pday"))
print (get_response(".pday"))
print (get_response(".pmonth"))
print (get_response(".done Task1"))
print (get_response(".done Adding date [23/11/21]"))
print (get_response(".pday"))
print (get_response(".pmonth"))
print (get_response(".aday"))
print (get_response(".amonth"))
"""

# Comment below code while tetsing


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()

    response_msg = get_response(msg)

    resp.message(response_msg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
