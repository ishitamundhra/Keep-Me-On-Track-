from sqlalchemy.sql.functions import mode
import datetime
import models
from database import SessionLocal, engine

# Adds task to the DB corresponding to the date, if present.
def add_task(task):

    db = SessionLocal()
    
    # Uncomment to create new model.
    # models.Base.metadata.create_all(bind=engine)

    # Default Date For the Task    
    date = datetime.datetime.today().strftime('%d/%m/%y')
    
    # Updates date&task with the date specified by the user, if present
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

    return "Task Added Successfully!!\U0001f604"

# Returns the list of pending task today.
def get_task():

    db = SessionLocal()

    todays_date = datetime.datetime.today().strftime('%d/%m/%y')
    taskList = db.query(models.Task).filter_by(date=todays_date, status="Pending").all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Woahhh!! Nothing pending Today.\n*YOU ARE ON TRACKK*"

    i = 1
    tasks = "Tasks to do today:\U0001f9D0\n"
    for task in taskList:
        tasks+= str(i) + ". "+task.task + "\n"
        i += 1

    return tasks

def get_months_task():
    db = SessionLocal()

    month = "___"+datetime.datetime.today().strftime('%m')+"%"
    taskList = db.query(models.Task).filter_by(status="Pending").filter(models.Task.date.like(month)).all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Woahhh!! Nothing pending this month.\n*YOU ARE ON TRACKK*"

    tasks = "Tasks pending this month:\U0001f9D0\n"
    taskList = sorted(taskList, key = lambda x: x.date)
    i = 1
    for task in taskList:
        tasks+= str(i) + ". " + task.task + " (Task was added on "+task.date+")\n"
        i += 1

    return tasks

# Marks the task, if present as done.
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
    print("Task Mark done.")

    db.commit()
    db.close()
    return "Task Mark Done successfully!!"

# Returns the task done by the user.
def get_done():

    db = SessionLocal()

    todays_date = datetime.datetime.today().strftime('%d/%m/%y')
    taskList = db.query(models.Task).filter_by(date=todays_date, status="Done").all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Get workin pal, dont't be lazy.\nHaven't done anything yet\U0001f480."

    tasks = "Work done today:\n"
    i = 1
    for task in taskList:
        tasks+= str(i) + ". " + task.task + "\n"
        i += 1

    tasks += "Good Going.\U0001f973"
    return tasks

# Returns task completed for the month.
def get_done_month():
    db = SessionLocal()

    month = "___"+datetime.datetime.today().strftime('%m')+"%"
    taskList = db.query(models.Task).filter_by(status="Done").filter(models.Task.date.like(month)).all()
    db.close()
    print(taskList)
    
    if taskList == []:
        return "Woahhh!! YOU HAVE DONE NOTHING. ABSOLUTELY NOTHING. This months.\n You better start working pal.\U0001f480."

    tasks = "Work completed this month: \n"
    i = 1
    for task in taskList:
        tasks+= str(i) + ". " + task.task +" from date "+task.date+"\n"
        i += 1
    
    tasks += "Great Going.\U0001f973"

    return tasks
