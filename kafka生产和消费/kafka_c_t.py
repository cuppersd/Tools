import json
from kafka import KafkaConsumer
consumer = KafkaConsumer('test_topic', auto_offset_reset='earliest', bootstrap_servers=['0.0.0.0:9092'])
# consumer = KafkaConsumer('message', auto_offset_reset='earliest', bootstrap_servers=['0.0.0.0:9092']) # , 172.19.224.60
# consumer.seek(partition, start)
print(consumer)
for msg in consumer:
    # print(msg.value)
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, (msg.value).decode())
    print(recv)
    # str_data = (msg.value).decode("utf-8", 'ignore')
    # print(str_data)
    # recv_data = json.loads(str_data)
    # print(type(recv_data))
    # print(recv_data)
    # recv_json = json.loads(str_data)
    # if recv_json['data']['msgtype'] == 'text':
    #     print(recv_json['data']['text']['content'])

