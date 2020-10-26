from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.structs import OffsetAndMetadata

kafkaConsumer = KafkaConsumer(bootstrap_servers=['0.0.0.0:9092'])

tp = TopicPartition('test_topic', 0)
kafkaConsumer.assign([tp])
kafkaConsumer.seek_to_beginning()
kafkaConsumer.seek(tp, 150000)
i =0
for msg in kafkaConsumer:
    print(msg.offset)
    i = i +1