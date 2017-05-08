# -*- coding : utf-8 -*-
from app import app, db
from app.client.models import *
from app.cmm.utils.date_utils import ep_trans_time

import pandas as pd
from app.cmm.utils.decimal_jsonizer import fn_jsonify


class RmEndpointDataMapper(object):
    @staticmethod
    def query_ep_data():
        return '''
SELECT 
    a.ep_id
    , a.ep_day
    , a.ep_time
    , a.ep_sec
    , cast(a.ep_data as DECIMAL(10,2)) as 'ep_data'
    , a.ep_offset
    , a.ep_part
    , a.create_dt
FROM
    RM_ENDPOINT_DATA AS a
    INNER JOIN    (
    SELECT ep_id, ep_day, ep_time, MAX(ep_sec) max_sec  FROM RM_ENDPOINT_DATA
    WHERE ep_day = :ep_day AND ep_id = :ep_id
    GROUP BY ep_id , ep_day , ep_time) AS b 
    ON  a.ep_id = b.ep_id
        AND a.ep_day = b.ep_day
        AND a.ep_time = b.ep_time
        AND a.ep_sec = b.max_sec
    INNER JOIN CM_TIME c 
    ON a.ep_time = c.time_key AND c.time_type = :time_type
ORDER BY a.ep_day  , a.ep_time , a.ep_sec
'''

class RmEndpointDataHandler(object):
    
    @staticmethod
    def do_save(param=None):
        print(param)
        if param.get('result') == False:
            return False
        try:
            data = RM_ENDPOINT_DATA()
            data.ep_id = param.get('ep_id')
            data.ep_day, data.ep_time, data.ep_sec = ep_trans_time(param.get('ep_time'))
            data.ep_data = param.get('ep_value')
            data.ep_part = param.get('partition')
            data.ep_offset = param.get('offset')
            data.create_dt = db.func.current_timestamp()
            db.session.add(data)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_chart_ep_data(param={}):
        try:
            rows = db.session.query(RM_ENDPOINT_DATA) \
                    .from_statement(RmEndpointDataMapper.query_ep_data()) \
                    .params(param) \
                    .all()
                    
            df = pd.DataFrame.from_records([ x.__dict__ for x in rows])
            df.ep_data = df.ep_data.astype(float).fillna(0.0)
            return {
                'ep_time' : df.ep_time.tolist()
                , 'ep_data' : df.ep_data.round(2).tolist()
            }
        except Exception as e:
            return {
                'ep_time' : []
                ,'ep_data' : []
            }

    @staticmethod
    def find_endpoint(param=[]):
        ep = db.session.query(OB_ENDPOINT) \
            .filter(OB_ENDPOINT.ep_id == '6725b7683e5e40eab77a87cef3c6c421') \
            .all()
        result = ob_endpoint_many.dump(ep)
        return result.data

    @staticmethod
    def get_dashboard(param=None):
        data = RmEndpointDataHandler.get_chart_ep_data(param)
        return data


class VmObObjectHandler(object):
    @staticmethod
    def get_gateways(rc_id=None):    
        buf = []
        if rc_id is None or len(rc_id) is not 32:
            return buf 
        try:
            query = db.session.query(VW_OB_OBJECTS.gw_name) # @UndefinedVariable)
            query = query.filter(VW_OB_OBJECTS.rc_id == rc_id) \
                    .group_by(VW_OB_OBJECTS.gw_name).all()  # @UndefinedVariable
            return [ dict([ ('gw_name',x.gw_name) ]) for x in query ]
        except Exception as e:
            return []

    @staticmethod
    def get_devices(rc_id=None):    
        buf = []
        if rc_id is None or len(rc_id) is not 32:
            return buf 
        try:
            query = db.session.query(VW_OB_OBJECTS.gw_name,VW_OB_OBJECTS.dev_name) # @UndefinedVariable)
            query = query.filter(VW_OB_OBJECTS.rc_id == rc_id) \
                    .group_by(VW_OB_OBJECTS.gw_name,VW_OB_OBJECTS.dev_name).all()  # @UndefinedVariable
            return [ dict([
                    ('gw_name',x.gw_name)
                    , ('dev_name',x.dev_name)]) for x in query ]
        except Exception as e:
            return []
    
    @staticmethod
    def get_endpoints(rc_id=None):
        buf = []
        if rc_id is None or len(rc_id) is not 32:
            return buf 
        try:
            query = db.session.query(VW_OB_OBJECTS) # @UndefinedVariable)
            query = query.filter(VW_OB_OBJECTS.rc_id == rc_id) \
                    .order_by(VW_OB_OBJECTS.gw_name, VW_OB_OBJECTS.dev_name).all()
            return [ dict([
                    ('ep_id',x.ep_id)
                    , ('ep_type',x.ep_type)
                    , ('ep_name',x.ep_name)
                    , ('gw_name',x.gw_name)
                    , ('dev_name',x.dev_name)]) for x in query ]
        except Exception as e:
            return []        
        
    @staticmethod
    def get_endpoint_detail(ep_id=None):
        r = db.session.query(OB_ENDPOINT).filter(OB_ENDPOINT.ep_id == ep_id).one()
        result = ob_endpoint_single.dump(r)
        return result.data
    
    @staticmethod
    def get_device_detail(dev_id=None):
        pass

    @staticmethod
    def get_gateway_detail(gw_id=None):
        pass
    
    
    