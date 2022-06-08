import logging
import os
import requests
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from slack import WebClient
from slack.errors import SlackApiError

def sendMessage(connection,queue,output):

    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection, logging_enable=True)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=queue)
        with sender:
            message = ServiceBusMessage(output)
            sender.send_messages(message)
    print(output)
    print("Done sending messages")
    print("-----------------------")

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
# ID of the channel you want to send the message to
channel_id = "C03KA7PSH88"

CONNECTION_STR = "Endpoint=sb://service-bus-1704.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=BTEYPRWJwh/okUp12fNpRhf0ccoZAVYRX1IKLte4Fbo="
QUEUE_NAME = "highpriority"

servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

def send_slack_message(message):
    payload = '{"text":"%s"}' %message
    response = requests.post('https://hooks.slack.com/services/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',
                              data = payload)
    print(response.text)

with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
    with receiver:
        for msg in receiver:
            print("Received: " + str(msg))
            send_slack_message(msg)
            receiver.complete_message(msg)