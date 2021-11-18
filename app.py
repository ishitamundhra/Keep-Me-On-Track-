from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


def get_response(msg):
    if msg == ".intro":
        return "welcome To Keep Me On Track Bot. The bot is built using twilio and flask, ans is deployed on heroku"
    elif msg == ".help":
        return "Still working on this"
    
    return "Woops idk what that means!!Sorreyy"




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