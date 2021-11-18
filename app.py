from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")

def hello():
    return "Hello, World!"

"""
1. .intro - about the bot && user.
2. .pday / .pending - Work left for today.
3. .add {task} {DD/MM/YYYY} - adds task in the above format.
4. .done {task} - Should be sth left today && should be in the list else given an error message.
5. .pmonth - Work left for the month.
6. .aday / .done - Work done today.
7. .amonth - Work done this month.
8. .help - informs about the available options
9. .done {task} {DD/MM/YY} - done on that day.

Can add on more to see sth like stats. will come back later to this.
"""

"""
Ideas:

We use dictionaries to add pending tasks corrseponding to dates, to decrease complexities.
"""

intro = """
Welcome To Keep Me On Track Bot.
The bot is built using twilio and flask, it's deployed on heroku.
To know more about the available features enter '.help'.
"""

help = """
1. .intro - about the bot && user.
2. .pday / .pending - Work left for today.
3. .add [task] [DD/MM/YYYY] - adds task in the above format.
4. .done [task] - Should be sth left today && should be in the list else given an error message.
5. .pmonth - Work left for the month.
6. .aday / .done - Work done today.
7. .amonth - Work done this month.
8. .help - informs about the available options
9. .done [task] [DD/MM/YY] - done on that day.
"""

default_msg = "Woops idk what that means!! Sorreyy!!!\nTry '.help' to understand me better *insert puppy face*."

pending_task = []
 
def get_response(msg):
    if msg == ".intro":
        return intro
    elif msg == ".help":
        return help
    elif msg[0:4] == ".add":
        pending_task.append(msg[5:])
        return "Added successfully"
    elif msg[0:5] == ".pday":
        tasks = ""
        for p in pending_task:
            tasks+=p+"\n"
        return tasks

    return default_msg

# print (get_response(".add Task1"))
# print (get_response(".add Task2"))
# print (get_response(".pday"))


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
