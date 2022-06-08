from flask import Flask, jsonify, request, make_response
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from myServiceBus import sendMessage
import logging
import os

app = Flask(__name__)
app.config["DEBUG"] = True

#Creating an in-memory data structure for demonstration purposes
issues = [
    {
        "id": 1,
        "title": "Ron is vomiting slugs again",
        "house": "Gryffindor",
        "priority": "High"
    },
    {
        "id": 2,
        "title": "Hermione has lost her Potions textbook",
        "house": "Gryffindor",
        "priority": "Medium"
    },
    {
        "id": 3,
        "title": "Harry's dorm is messy",
        "house": "Gryffindor",
        "priority": "Low"
    },
    {
        "id": 4,
        "title": "The Basilisk is on the loose",
        "house": "Slytherin",
        "priority": "High"
    },
    {
        "id": 5,
        "title": "Draco has been punched in the face",
        "house": "Slytherin",
        "priority": "Medium"
    }
]

@app.route('/', methods=['GET']) #tell which HTTP method we are using (GET) and what route (extra bit of the URL) this method will be activated on.  In this case nothing and so home
def home():
    output = "<h1>Welcome to the Hogwarts issue sorting program.</h1>"
    return output

# Implementing logging to a file
@app.before_first_request
def before_first_request():
    log_level = logging.INFO

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)

    app.logger.setLevel(log_level)

    defaultFormatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(defaultFormatter)


@app.route("/api", methods=['GET', 'POST'])
def triage_bugs():

    if request.method == 'GET':
        for issue in issues:
            if issue['priority'] not in {"High", "Medium", "Low"}:
                app.logger.info(issue)

        return jsonify({'issues': issues})

    if request.method == 'POST':
        #Validating the API request
        if not request.json or not 'priority' in request.json or request.json['priority'] not in {"High", "Medium", "Low"}:
            app.logger.info(request.json)
            return 'Bad request! This event has been logged.', 400

        if request.json['priority'] == "High":
            
            CONNECTION_STR = "Endpoint=sb://service-bus-1704.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=BTEYPRWJwh/okUp12fNpRhf0ccoZAVYRX1IKLte4Fbo="
            QUEUE_NAME = "highpriority"
            sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

        else:

            CONNECTION_STR = "Endpoint=sb://service-bus-1704.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=BTEYPRWJwh/okUp12fNpRhf0ccoZAVYRX1IKLte4Fbo="
            QUEUE_NAME = "generalbugs"
            sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

        return request.json

if __name__ == '__main__':
    app.run()