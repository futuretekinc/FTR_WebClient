import json
from app import app,KAFKA_HOST
from kafka.client import KafkaClient
from kafka import KafkaConsumer,KafkaProducer,SimpleProducer,SimpleConsumer
from kafka import KafkaProducer,KafkaClient,TopicPartition
from datetime import datetime
import threading

 
def kafka_json_producer():
    return KafkaProducer(bootstrap_servers=KAFKA_HOST,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def kafka_json_consumer():
    return KafkaConsumer(bootstrap_servers=KAFKA_HOST,auto_offset_reset='earliest',value_deserializer = lambda m: json.loads(m.decode('utf-8')))

def kafka_send_no_lock(_topic, dict_message):
    if isinstance(dict_message,dict):
        producer = kafka_json_producer()
        future = producer.send(_topic,dict_message)
        record_meta = future.get(timeout=30)
        producer.close(timeout=10)
        return { 'result' : True
            , 'topic' : record_meta.topic
            , 'partition' : record_meta.partition
            , 'offset' : record_meta.offset 
        }
    else:
        return { 'result' : False
                    , 'error' : 'TypeError'
                    , 'message' : dict_message
            }
        
def kafka_send(_topic, dict_message):
    if isinstance(dict_message,dict):
        lock  = threading.Lock()
        with lock:        
            producer = kafka_json_producer()
            future = producer.send(_topic,dict_message)
            record_meta = future.get(timeout=30)
            producer.close(timeout=10)
            return { 'result' : True
                    , 'topic' : record_meta.topic
                    , 'partition' : record_meta.partition
                    , 'offset' : record_meta.offset 
            }
    else:
        return { 'result' : False
                    , 'error' : 'TypeError'
                    , 'message' : dict_message
            }

def kafka_poll(_topic,poll_size=1,_offset=0,_partition=0,poll_timeout_ms=1000):
    buf = []
    lock  = threading.Lock()
    with lock:
        consumer = kafka_json_consumer()
        tp = TopicPartition(_topic,_partition)
        consumer.assign([tp])
        consumer.seek(tp,_offset)
        records = consumer.poll(poll_timeout_ms,poll_size)
        for record in records.values():
            print(record)
            for x in record:
                buf.append({
                    'topic' : x.topic
                    , 'partition' : x.partition
                    , 'offset' : x.offset
                    , 'value' : x.value
                })
        consumer.close()
    return buf
        
         
def kafka_test():
    lock  = threading.Lock()
    with lock:
        msg = 'message testing!!!!222 ' + str(datetime.now().time())
        producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)
        producer.send('my_favorite_topic',bytes(msg,'utf-8'))
        producer.close(timeout=5)
        print('done')
        

def kafka_test_consume_standby():    
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOST,auto_offset_reset='earliest',value_deserializer = lambda m: json.loads(m.decode('utf-8')))
#     consumer.subscribe(['my_favorite_topic'])
    tp = TopicPartition('my_favorite_topic',0)
    consumer.assign([tp])
    consumer.seek(tp,1048)
    records = consumer.poll(500,20)
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

import numpy as np

if __name__ == '__main__':
#     kafka_test_consume_standby()
    _topic = '11d764dccdad4977a885104787bef3f8'
    
    r = kafka_poll(_topic,poll_size=10,_offset=4,_partition=0,poll_timeout_ms=10000)
    for x in r:
        print(x)
#     r = kafka_poll(_topic,100,0)
#     print(r)