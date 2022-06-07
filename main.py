# import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://service-bus-1704.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=BTEYPRWJwh/okUp12fNpRhf0ccoZAVYRX1IKLte4Fbo="
QUEUE_NAME = "highpriority"

def send_single_message(sender):
    message = ServiceBusMessage("Hello World")
    sender.send_messages(message)
    print("Hello World")

servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
    with sender:
        send_single_message(sender)

print("Done sending messages")
print("-----------------------")