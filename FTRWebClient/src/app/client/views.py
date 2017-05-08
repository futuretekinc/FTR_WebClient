import threading
from app import app,db
from datetime import datetime
from flask import request,redirect,url_for
from flask.views import MethodView
from flask.templating import render_template

from wtforms import Form, StringField, validators , HiddenField,SelectField,DateField
from app.client.service.kafka_handler import kafka_send, kafka_poll
from app.cmm.utils.decimal_jsonizer import fn_jsonify
from app.client.models import RM_ENDPOINT_DATA,CM_CODED
from app.cmm.utils.date_utils import ep_trans_time
from app.client.service.endpoint_data_service import RmEndpointDataHandler


class DASHBOARD_FORM(Form):
    ep_id = StringField(u'엔드포인트id',[validators.required(), validators.Length(min=32,max=32)]) 
    time_type = SelectField(u'시간 타입',choices=[('','NONE')],render_kw={'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    time_day = DateField(u'날짜선택', format="%Y-%m-%d",default=datetime.today,validators=[validators.required()],render_kw={'type' : 'date' })
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.time_type.choices = self.time_type_choice()

    def time_type_choice(self):
        comm_code = 'TIME_TYPE'
        rows = db.session.query(CM_CODED).filter(CM_CODED.comm_code == comm_code).all()  # @UndefinedVariable
        buf = []
        for x in rows:
            buf.append((x.comd_code, x.comd_cdnm))
        return buf    
    

class KAFKA_PRODUCER_FORM(Form):
    ep_id = StringField(u'엔드포인트id(TOPIC)',[validators.required(), validators.Length(min=32,max=32)],render_kw={'value' : '11d764dccdad4977a885104787bef3f8'})
    ep_value = StringField(u'값', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" }) 
    ep_time = HiddenField()
    
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
        print("form-data->")
        print(form.data)
        if form.validate():
            param = form.data
            print(param)
            topic = param.get('ep_id')
            ret = kafka_send(topic,param)
            param.update(ret)
            issave = RmEndpointDataHandler.do_save(param)
#             print("issave=>{}".format(issave))
            return redirect(url_for('client.kaf_prod'))
            
        return render_template('client/kaf_prod.html',form=form)
    
    
    
    
    
    
    
    
    
    