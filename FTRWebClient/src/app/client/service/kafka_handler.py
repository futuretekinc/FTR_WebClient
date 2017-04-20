import json
from app import app,producer,KAFKA_HOST
from kafka.client import KafkaClient
from kafka import KafkaConsumer,KafkaProducer,SimpleProducer,SimpleConsumer
from kafka import KafkaProducer,KafkaClient,TopicPartition
from datetime import datetime
import threading

def kafka_test():
    lock  = threading.Lock()
    with lock:
        msg = 'message testing!!!!222 ' + str(datetime.now().time())
        producer.send('my_favorite_topic',bytes(msg,'utf-8'))
        print('done')

def kafka_test_consume_standby():    
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOST,auto_offset_reset='earliest',value_deserializer = lambda m: json.loads(m.decode('utf-8')))
#     consumer.subscribe(['my_favorite_topic'])
    tp = TopicPartition('my_favorite_topic',0)
    consumer.assign([tp])
    consumer.seek(tp,1048)
    records = consumer.poll(10000,20)
    for record in records.values():
        for x in record:
            print(type(x.value))
            print(x.value.get('A'))
            print(x.value.get('B'))
            print(x.value.get('C'))
        
# for idx,message in enumerate(consumer):
#         print (idx," %s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                           message.offset, message.key,
#                                           message.value))    
#     consumer.close()


if __name__ == '__main__':
    kafka_test_consume_standby()