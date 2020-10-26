import pickle
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['0.0.0.0:9092'],
                         key_serializer=lambda k: pickle.dumps(k),
                         value_serializer=lambda v: pickle.dumps(v))

start_time = time.time()
for i in range(0, 10000):
    print('------{}---------'.format(i))
    future = producer.send('test_topic', key='num', value=i, partition=0)

# 将缓冲区的全部消息push到broker当中
producer.flush()
producer.close()
 
end_time = time.time()
time_counts = end_time - start_time
print(time_counts)