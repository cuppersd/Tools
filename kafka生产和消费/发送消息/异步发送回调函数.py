import pickle
import time
from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers=['0.0.0.0:9092'],
                         key_serializer=lambda k: pickle.dumps(k),
                         value_serializer=lambda v: pickle.dumps(v)
                        )


def on_send_success(*args, **kwargs):
	print("on_send_success")
	print(args[0].topic)
	print(args[0].partition)
	return args


def on_send_error(*args, **kwargs):
	print("on_send_error")
	return args


start_time = time.time()
for i in range(0, 10000):
    print('------{}---------'.format(i))
    producer.send('original_topic', key='num', value=i).add_callback(on_send_success).add_errback(on_send_error)


producer.flush()
producer.close()


end_time = time.time()
time_counts = end_time - start_time
print(time_counts)