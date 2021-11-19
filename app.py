from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import utils

"""
Features:

1. .intro - about the bot && user. [DONE]
2. .pday / .pending - Work left for today. [DONE]
3. .add {task} Optional[DD/MM/YY] - adds task in the above format. [DONE]
4. .done {task} Optional[DD/MM/YY] - Should be sth left today && should be in the list else given an error message. [DONE]
5. .pmonth - Work left for the month. [DONE]
6. .aday / .done - Work done today. [DONE]
7. .amonth - Work done this month. [DONE
8. .help - informs about the available options [DONE]

Can add on more to see sth like stats. will come back later to this.
"""

"""
Ideas:

Split this file to utils.py. [DONE]
Add emojis maybe. [DONE]
Clean up the code. [DONE]
Try hosting the db in heroku or swith to heroku db - because test.db changes everytime changes are commited.(would .gitignore help?)
"""

intro = """
Welcome To Keep Me On Track Bot. \U0001f607
The bot is built using twilio and flask, it's deployed on heroku.
To know more about the available features enter '.help'.
"""

help = """
1. .intro - About the bot && user.
2. .pday / .pending - Work left for today.
3. .add [task] optional[DD/MM/YY] - Adds task.
4. .done [task] optional[DD/MM/YY]- Marks the task as done, if present.
5. .pmonth - Work left for the month.
6. .aday / .done - Work done today.
7. .amonth - Work done this month.
8. .help - Overview of the features.
"""

default_msg = "Woops idk what that means!! Sorreyy!!!\U0001f915\nTry '.help' to understand me better.\U0001f62c"

# Returns the response based on user's message.
def get_response(msg):

    if msg == ".intro":
        return intro
    elif msg == ".help":
        return help
    elif msg[0:4] == ".add":
        return utils.add_task(msg[5:])
    elif msg[0:5] == ".pday" or msg[0:9]==".pending":
        return utils.get_task()
    elif msg[0:7] == ".pmonth":
        return utils.get_months_task()
    elif msg[0:5] == ".done":
        return utils.mark_done(msg[6:])
    elif msg[0:] == ".aday":
        return utils.get_done()
    elif msg[0:] == ".amonth":
        return utils.get_done_month()
    return default_msg

'''
# Uncomment below code while testing.
print (get_response(".intro"))
print (get_response("TEST"))
print (get_response(".add Finish adding basic features of 'Keep Me On Track'"))
print (get_response(".add Finish adding coding contest schedules [19/11/21]"))
print (get_response(".add Clean Up the code."))
print (get_response(".pday"))
print (get_response(".pmonth"))
print (get_response(".done Finish adding basic features of 'Keep Me On Track'"))
print (get_response(".pday"))
print (get_response(".pmonth"))
print (get_response(".aday"))
print (get_response(".amonth"))

# Comment below code while tetsing
'''

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    response_msg = get_response(msg)
    resp.message(response_msg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
