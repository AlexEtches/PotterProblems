from flask import Flask,request
from myServiceBus import *
import os

app = Flask(__name__)
app.config["DEBUG"] = True

CONNECTION_STR = os.getenv("CONNECTION_STRING")

@app.route('/', methods=['GET']) #tell which HTTP method we are using (GET) and what route (extra bit of the URL) this method will be activated on.  In this case nothing and so home
def home():
    output = "<h1>Welcome to the Hogwarts issue sorting program.</h1>"
    return output

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