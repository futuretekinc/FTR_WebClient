import threading
from app import app
from flask import request,redirect,url_for
from flask.views import View, MethodView
from flask.templating import render_template

from datetime import datetime 
from wtforms import Form,BooleanField, StringField, PasswordField, validators, IntegerField,SelectField,TextAreaField,DateField
from wtforms.validators import DataRequired, Required
from kafka.client import KafkaClient
from kafka import KafkaConsumer,KafkaProducer,SimpleProducer
from kafka import KafkaProducer
from app.client.service.kafka_handler import kafka_json_producer, kafka_send,\
    kafka_poll
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class KAFKA_PRODUCER_FORM(Form):
    ep_id = StringField(u'엔드포인트id(TOPIC)',[validators.required(), validators.Length(min=32,max=32)],render_kw={'value' : '11d764dccdad4977a885104787bef3f8'})
    ep_type = StringField(u'타입', [validators.required(),validators.Length(min=1,max=50)],render_kw={'value' : "습도센서" , 'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    ep_scale = StringField(u'스케일', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" })
    ep_value = StringField(u'값', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" }) 
    
class KAFKA_CONSUMER(MethodView):
    def poll(self):
        topic = request.values.get('topic')
        partition = request.values.get('partition')
        offset = request.values.get('offset')
        poll_size = request.values.get('poll_size')
        try:
            data = kafka_poll(_topic=topic,poll_size=int(poll_size),_offset=int(offset),_partition=int(partition),poll_timeout_ms=500)
            return fn_jsonify({'result' : True, 'data' : data })
        except Exception as e:
            print("[ERROR] - {}".format(str(e)))
            return fn_jsonify({'result' : False, 'error' : 'fetch fail'})
    
    def post(self):
        return self.poll()

    def get(self):
        return self.poll()

class KAFKA_PRODUCER(MethodView):
    def get(self):
        form = KAFKA_PRODUCER_FORM(request.form)
        return render_template('client/kaf_prod.html',form=form)
    
    def post(self):
        form = KAFKA_PRODUCER_FORM(request.form)
        if form.validate():
            param = form.data
            topic = param.get('ep_id')
            ret = kafka_send(topic,param)
            print(ret)
            return redirect(url_for('client.kaf_prod'))
            
        return render_template('client/kaf_prod.html',form=form)
    
    
    
    
    
    
    
    
    