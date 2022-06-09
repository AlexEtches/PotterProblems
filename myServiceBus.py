from azure.servicebus import ServiceBusClient, ServiceBusMessage

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