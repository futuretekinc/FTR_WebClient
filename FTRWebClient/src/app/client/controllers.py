# -*- coding : utf-8 -*-
from flask import abort
from app import db, render_template, send_from_directory
from flask import Response, jsonify, request,Blueprint,flash,redirect
from app.client.views import KAFKA_PRODUCER,KAFKA_CONSUMER,DASHBOARD_FORM
from app.client.models import *
from app.client.service.endpoint_data_service import *
from app.client.service.kafka_handler import kafka_send, kafka_send_no_lock
from app.cmm.utils.decimal_jsonizer import fn_jsonify
from flask_cache import Cache 

#cache = Cache(app)

client = Blueprint('client', __name__, url_prefix='/client')

# client.add_url_rule('/kaf_prod',view_func=KAFKA_PRODUCER().as_view('kaf_prod'))
# client.add_url_rule('/kaf_poll',view_func=KAFKA_CONSUMER().as_view('kaf_poll'))

@client.route("/intro")
def intro():
    abort(500)
    pass

@client.route("/gateway/<gwId>")
@client.route("/gateway")
def gateway_dashboard(gwId=None):
#     if gwId == None:
#         abort(500)
    gw_id = 'FTM20170601012345678901234567890'
    ep_ids = []    
    ep_day = '20170613'
    time_type = 'MIN_1'
    data = RmEndpointDataHandler.get_client_dashboard(gw_id, ep_ids, ep_day, time_type)        
    return render_template("client/gateway.html",data=data)

client.add_url_rule('/gateway', 'gateway' , gateway_dashboard)

@client.route("/data")
def gateway_data():
    gw_id = 'FTM20170601012345678901234567890'
    ep_ids = []    
    ep_day = '20170613'
    time_type = 'MIN_5'
    data = RmEndpointDataHandler.get_client_dashboard(gw_id, ep_ids, ep_day, time_type)        
    return fn_jsonify(data)


#@cache.cached(timeout=60) 
def dashboard():
    rc_id = 'RCFTMb650ac1514a23af4757411dcc4e'
    form = DASHBOARD_FORM(request.form)
    form.ep_id.data = 'RCFTMb650ac1514a23af4757411dcc4e'
    param = {
         'ep_day' : '20170612'
        ,'ep_id' : 'a917bacb24804e79ecf7deb9028a0431'
        ,'time_type':'MIN_15'
    }
    data = RmEndpointDataHandler.get_dashboard(param)
    data['object'] = VmObObjectHandler.view_data(rc_id)
    return render_template("client/dashboard.html",form=form,**data)

def chart_data():
    ep_day = request.values.get('ep_day','20170612',type=str)
    ep_id = request.values.get('ep_id','a917bacb24804e79ecf7deb9028a0431',type=str)
    time_type = request.values.get('time_type','MIN_15',type=str)
    param = {
         'ep_day' : ep_day.replace('-','')
        ,'ep_id' :  ep_id
        ,'time_type':time_type
    }
    data = RmEndpointDataHandler.get_dashboard(param)
    print("**data")
    print(param)
    print(data)
    print("**data")
    rc_id = 'RCFTMb650ac1514a23af4757411dcc4e'
    data['object'] = VmObObjectHandler.view_data(rc_id)
    return fn_jsonify(data)

def table_data():
    ep_day = request.values.get('ep_day','20170612',type=str)
    ep_id = request.values.get('ep_id','a917bacb24804e79ecf7deb9028a0431',type=str)
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
    
#@cache.cached(timeout=60) 
def checkbox():
    return render_template("client/check_box_table.html")

client.add_url_rule('/checkbox', 'checkbox' , checkbox)

if __name__ == '__main__':
    d = chart_data()
    print(d)