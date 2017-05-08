# -*- coding : utf-8 -*-
from app import db, render_template, send_from_directory
from flask import Response, jsonify, request,Blueprint,flash,redirect
from app.client.views import KAFKA_PRODUCER,KAFKA_CONSUMER,DASHBOARD_FORM
from app.client.models import *
from app.client.service.endpoint_data_service import *
from app.client.service.kafka_handler import kafka_send, kafka_send_no_lock
from app.cmm.utils.decimal_jsonizer import fn_jsonify

client = Blueprint('client', __name__, url_prefix='/client')

client.add_url_rule('/kaf_prod',view_func=KAFKA_PRODUCER().as_view('kaf_prod'))
client.add_url_rule('/kaf_poll',view_func=KAFKA_CONSUMER().as_view('kaf_poll'))

def dashboard():
    form = DASHBOARD_FORM(request.form)
    form.ep_id.data = '6725b7683e5e40eab77a87cef3c6c421'
    param = {
         'ep_day' : '20170508'
        ,'ep_id' : '6725b7683e5e40eab77a87cef3c6c421'
        ,'time_type':'MIN_15'
    }
    data = RmEndpointDataHandler.get_dashboard(param)
    return render_template("client/dashboard.html",form=form,**data)

def chart_data():
    ep_day = request.values.get('ep_day','20170508',type=str)
    ep_id = request.values.get('ep_id','6725b7683e5e40eab77a87cef3c6c421',type=str)
    time_type = request.values.get('time_type','MIN_15',type=str)
    param = {
         'ep_day' : ep_day.replace('-','')
        ,'ep_id' :  ep_id
        ,'time_type':time_type
    }
    data = RmEndpointDataHandler.get_dashboard(param)
    return fn_jsonify(data)

client.add_url_rule('/dashboard', 'dashboard' , dashboard)
client.add_url_rule('/chart_data', 'chart_data' , chart_data)

@client.route("/prod_test",methods=['GET','POST'])
def prod_test():
    try:
        param = {}
        param['ep_id'] = request.args.get('ep_id')
        param['ep_time'] = request.args.get('ep_time')
        param['ep_value'] = request.args.get('ep_value')
        topic = param.get('ep_id')
        ret = kafka_send_no_lock(topic,param)
        param.update(ret)
        issave = RmEndpointDataHandler.do_save(param)
        return fn_jsonify({'result' : issave })
    except Exception as e:
        print(e)
        return fn_jsonify({'result' : False, 'error' : str(e) })
    
