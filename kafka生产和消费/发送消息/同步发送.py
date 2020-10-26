import pickle
import time
from kafka import KafkaProducer
from kafka.errors import kafka_errors

producer = KafkaProducer(bootstrap_servers=['0.0.0.0:9092'],
                         key_serializer=lambda k: pickle.dumps(k),
                         value_serializer=lambda v: pickle.dumps(v)
                         )


start_time = time.time()
for i in range(0, 10000):
    print('------{}---------'.format(i))
    future = producer.send('test_topic', key='num', value=i, partition=0)
    try:
        record_metadata = future.get(timeout=10)
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)
    except kafka_errors as e:
        print(str(e))
 
end_time = time.time()
time_counts = end_time - start_time
print(time_counts)