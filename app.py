from flask import Flask,request
from myServiceBus import *
import logging
import os

app = Flask(__name__)
app.config["DEBUG"] = True

CONNECTION_STR = "Endpoint=sb://service-bus-1704.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=BTEYPRWJwh/okUp12fNpRhf0ccoZAVYRX1IKLte4Fbo="

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


@app.route("/api", methods=['POST'])
def triage_bugs():

    #Validating the API request
    if not request.json or not 'title' in request.json or not 'house' in request.json or not 'priority' in request.json\
    or request.json['priority'] not in {"High", "Medium", "Low"}\
    or request.json['house'] not in {"Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"}:
        QUEUE_NAME = "invalidrequests"
        sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

    elif request.json['priority'] == "High":
        QUEUE_NAME = "highpriority"
        sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

    else:
        QUEUE_NAME = "generalbugs"
        sendMessage(CONNECTION_STR,QUEUE_NAME,str(request.json))

    return request.json

if __name__ == '__main__':
    app.run()