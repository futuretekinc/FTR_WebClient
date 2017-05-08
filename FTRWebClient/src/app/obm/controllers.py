# -*- coding : utf-8 -*-
from flask import Response, jsonify, request, Blueprint, flash, redirect
from flask.views import MethodView

from app import db, render_template, send_from_directory
from app.client.service.endpoint_data_service import RmEndpointDataHandler
from app.client.service.kafka_handler import kafka_send, kafka_send_no_lock
from app.client.views import KAFKA_PRODUCER, KAFKA_CONSUMER
from app.cmm.utils.decimal_jsonizer import fn_jsonify


obm = Blueprint('obm', __name__, url_prefix='/obm')

'''자원상세정보조회 '''

class V_RC_DETAIL(MethodView):
    def post(self):
        return fn_jsonify({})
    
obm.add_url_rule('/rc_detail',view_func=V_RC_DETAIL().as_view('rc_detail'))


'''게이트웨이 목록 조회'''

class V_GW_LIST(MethodView):
    def post(self):
        return fn_jsonify({})

obm.add_url_rule('/gw_list',view_func=V_GW_LIST().as_view('gw_list'))


'''게이트웨이 상세정보 조회'''

class V_GW_DETAIL(MethodView):
    def post(self):
        return fn_jsonify({})

obm.add_url_rule('/gw_detail',view_func=V_GW_DETAIL().as_view('gw_detail'))



'''엔드포인트 목록 조회'''

class V_EP_LIST(MethodView):
    def post(self):
        return fn_jsonify({})

obm.add_url_rule('/ep_list',view_func=V_EP_LIST().as_view('ep_list'))


'''엔드포인트 상세 조회'''
class V_EP_DETAIL(MethodView):
    def post(self):
        return fn_jsonify({})

obm.add_url_rule('/ep_detail',view_func=V_EP_DETAIL().as_view('ep_detail'))


'''엔드포인트 상태정보 조회'''
class V_EP_STATUS(MethodView): pass
obm.add_url_rule('/ep_status',view_func=V_EP_STATUS().as_view('ep_status'))


'''엔드포인트 설정 정보 조회'''
class V_EP_CONFIG(MethodView): pass
obm.add_url_rule('/ep_config',view_func=V_EP_CONFIG().as_view('ep_config'))


'''엔드포인트 설정 정보 업데이트 '''
class V_EP_UPDATE(MethodView): pass
obm.add_url_rule('/ep_update',view_func=V_EP_UPDATE().as_view('ep_update'))


''' 테이블 및 차트 데이터 요청 '''
class V_EP_DATA(MethodView): pass
obm.add_url_rule('/ep_data',view_func=V_EP_DATA().as_view('ep_data'))


'''엔드포인트 조회 조건 저장'''
class V_EP_OPTION(MethodView): pass
obm.add_url_rule('/ep_option',view_func=V_EP_OPTION().as_view('ep_option'))




















