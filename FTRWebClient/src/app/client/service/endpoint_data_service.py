# -*- coding : utf-8 -*-
from app import app, db
from app.client.models import *
from app.cmm.utils.date_utils import ep_trans_time

import pandas as pd
from app.cmm.utils.decimal_jsonizer import fn_jsonify
from sqlalchemy.sql.expression import desc


class RmEndpointDataMapper(object):
    @staticmethod
    def query_ep_data():
        return '''
SELECT 
    a.ep_id
    , a.ep_day
    , a.ep_time
    , a.ep_sec
    , a.ep_unix
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
    def get_client_dashboard(gw_id, ep_ids, ep_day, time_type):
        gw = {}
        try:
            gw = RmEndpointDataHandler.load_gateway(gw_id)
            gw['date'] = ep_day
            gw['time_type'] = time_type
            ep_infos = RmEndpointDataHandler.load_endpoints(gw_id,ep_ids)
            buf = []
            for ep_info in ep_infos:
                ep, ctime, cdata, tdata  = RmEndpointDataHandler.load_endpoint_data(ep_info, ep_day, time_type)
                if len(ctime) > 0:
                    buf.append(dict([('endpoint',  ep), ('chart_time', ctime), ('chart_data', cdata), ('table_data', tdata)]))
            result =  {'gateway' : gw,'dashboard' : buf, 'result' : 'succ'}
            return result
        except Exception as e:
            return {'gateway' : gw, 'dashboard' : [], 'result' : 'fail', 'error' : str(e) }
    
    @staticmethod
    def load_gateway(gw_id):
        try:
            gw = db.session.query(OB_GATEWAY).filter(OB_GATEWAY.gw_id == gw_id).one()
            return { 'id' :  gw.gw_id, 'name' : gw.gw_name } 
        except Exception as e:
            raise e
    
    @staticmethod
    def load_endpoints(gw_id,ep_ids=[]):
        try:
            rows = db.session.query(OB_ENDPOINT) \
                .join(OB_DEVICE_MAP, OB_DEVICE_MAP.ep_id == OB_ENDPOINT.ep_id) \
                .join(OB_GATEWAY_MAP, OB_GATEWAY_MAP.dev_id == OB_DEVICE_MAP.dev_id) \
                .filter(OB_GATEWAY_MAP.gw_id == gw_id)
            if ep_ids and len(ep_ids) > 0:
                rows = rows.filter(OB_ENDPOINT.ep_id.in_(ep_ids))
            rows = rows.all()
            result = ob_endpoint_many.dump(rows)
            return result.data
        except Exception as e:
            return []

    @staticmethod
    def load_endpoint_data(ep_info, ep_day, time_type):
        try:
            ep_id = ep_info.get('ep_id')
            subq = (db.session.query(func.max(RM_ENDPOINT_DATA.ep_sec).label('max_sec')).group_by(RM_ENDPOINT_DATA.ep_day, RM_ENDPOINT_DATA.ep_time))
            subq = subq.filter(RM_ENDPOINT_DATA.ep_day == ep_day).filter(RM_ENDPOINT_DATA.ep_id == ep_id).subquery()
        
            rows = db.session.query(RM_ENDPOINT_DATA).join(subq, RM_ENDPOINT_DATA.ep_sec == subq.c.max_sec) 
            rows = rows.filter(RM_ENDPOINT_DATA.ep_day== ep_day )
            rows = rows.filter(RM_ENDPOINT_DATA.ep_id == ep_id ) 
            rows = rows.join(CM_TIME, CM_TIME.time_key == RM_ENDPOINT_DATA.ep_time)
            rows = rows.filter(CM_TIME.time_type==time_type).order_by(desc(RM_ENDPOINT_DATA.ep_time)).limit(600).all()
            result = rm_endpoint_data_many.dump(rows)        
            print(result.data)
            df = pd.DataFrame.from_records([ x.__dict__ for x in rows])
            df.ep_data = df.ep_data.astype(float).fillna(0.0)
            return (ep_info, df.ep_unix.tolist(), df.ep_data.round(2).tolist(), result.data)
#             return {
#                 'ep_time' : df.ep_time.tolist()
#                 , 'ep_data' : df.ep_data.round(2).tolist()
#                 , 'table' : result.data
#             }
        except Exception as e:
            print("** " + str(e))
            return (None,[],[],[])
             
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
            result = rm_endpoint_data_many.dump(rows)        
            df = pd.DataFrame.from_records([ x.__dict__ for x in rows])
            df.ep_data = df.ep_data.astype(float).fillna(0.0)
            return {
                'ep_time' : df.ep_time.tolist()
                , 'ep_data' : df.ep_data.round(2).tolist()
                , 'table' : result.data
            }
        except Exception as e:
            print(e)
            return {
                'ep_time' : []
                ,'ep_data' : []
                , 'table' : []
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
    def view_data(rc_id):
        r = {}
        r['gateways'] = VmObObjectHandler.get_gateways(rc_id)
        r['devices'] = VmObObjectHandler.get_devices(rc_id)
        r['endpoints'] = VmObObjectHandler.get_endpoints(rc_id)
        return r

    @staticmethod
    def get_gateways(rc_id=None):    
        buf = []
        if rc_id is None or len(rc_id) is not 32:
            return buf 
        try:
            query = db.session.query(VW_OB_OBJECTS.gw_name,VW_OB_OBJECTS.gw_id) # @UndefinedVariable)
            query = query.filter(VW_OB_OBJECTS.rc_id == rc_id) \
                    .group_by(VW_OB_OBJECTS.gw_name,VW_OB_OBJECTS.gw_id).all()  # @UndefinedVariable
            return [ dict([ ('gw_name',x.gw_name),('gw_id',x.gw_id) ]) for x in query ]
        except Exception as e:
            return []

    @staticmethod
    def get_devices(rc_id=None):    
        buf = []
        if rc_id is None or len(rc_id) is not 32:
            return buf 
        try:
            query = db.session.query(VW_OB_OBJECTS.gw_id,VW_OB_OBJECTS.gw_name,VW_OB_OBJECTS.dev_id,VW_OB_OBJECTS.dev_name) # @UndefinedVariable)
            query = query.filter(VW_OB_OBJECTS.rc_id == rc_id) \
                    .group_by(VW_OB_OBJECTS.gw_id,VW_OB_OBJECTS.gw_name,VW_OB_OBJECTS.dev_id,VW_OB_OBJECTS.dev_name).all()  # @UndefinedVariable
            return [ dict([
                    ('gw_name',x.gw_name),('gw_id',x.gw_id)
                    , ('dev_name',x.dev_name),('dev_id', x.dev_id)]) for x in query ]
        except Exception as e:
            print(e)
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
                    , ('dev_name',x.dev_name),('dev_id',x.dev_id)]) for x in query ]
        except Exception as e:
            return []        
        
    @staticmethod
    def get_endpoint_detail(ep_id=None):
        r = db.session.query(OB_ENDPOINT).filter(OB_ENDPOINT.ep_id == ep_id).one()
        result = ob_endpoint_single.dump(r)
        return result.data
    
    @staticmethod
    def get_device_detail(dev_id=None):
        r = db.session.query(OB_DEVICE).filter(OB_DEVICE.dev_id == dev_id).one()
        result = ob_device_single.dump(r)
        return result.data

    @staticmethod
    def get_gateway_detail(gw_id=None):
        r = db.session.query(OB_GATEWAY).filter(OB_GATEWAY.gw_id == gw_id).one()
        result = ob_gateway_single.dump(r)
        return result.data
    
    
    