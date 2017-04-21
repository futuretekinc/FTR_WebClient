# -*- coding : utf-8 -*-
from app import app, db
from app.client.models import *
from app.cmm.utils.date_utils import ep_trans_time

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