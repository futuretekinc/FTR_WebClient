# -*- coding : utf-8 -*-
from app import db, render_template, send_from_directory
from flask import Response, jsonify, request,Blueprint,flash,redirect
from app.client.views import KAFKA_PRODUCER,KAFKA_CONSUMER
from app.client.service.kafka_handler import kafka_send, kafka_send_no_lock
from app.client.service.endpoint_data_service import RmEndpointDataHandler
from app.cmm.utils.decimal_jsonizer import fn_jsonify

client = Blueprint('client', __name__, url_prefix='/client')

client.add_url_rule('/kaf_prod',view_func=KAFKA_PRODUCER().as_view('kaf_prod'))
client.add_url_rule('/kaf_poll',view_func=KAFKA_CONSUMER().as_view('kaf_poll'))


def dashboard():
    return render_template("client/dashboard.html")

client.add_url_rule('/dashboard', 'dashboard' , dashboard)

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