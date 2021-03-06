from kafka import KafkaConsumer
import json
import sys

topic = sys.argv[1]
print(topic)
# Setup kafka consumer, subscribes to a topic. Auto offset only set for testing
consumer = KafkaConsumer(topic,bootstrap_servers=['sandbox-hdp.hortonworks.com:6667'],
	#value_deserializer=lambda x:json.loads(x.decode('utf-8')),
	auto_offset_reset='earliest')

for msg in consumer:
	print(msg)

