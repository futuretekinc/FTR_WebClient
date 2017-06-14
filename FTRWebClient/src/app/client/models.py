from sqlalchemy import Table,Column,NVARCHAR,Integer,func
from app import db
from marshmallow_sqlalchemy import ModelSchema

class RM_ENDPOINT_DATA(db.Model):
    __tablename__ = "RM_ENDPOINT_DATA"
    __table_args__ = {
        'autoload' : True,
#         'schema' : 'appdb',
        'autoload_with': db.engine
    }
class CM_CODEM(db.Model):
    __tablename__ = "CM_CODEM"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }
    
class CM_CODED(db.Model):
    __tablename__ = "CM_CODED"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class OB_ENDPOINT(db.Model):
    __tablename__ = "OB_ENDPOINT"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class OB_DEVICE(db.Model):
    __tablename__ = "OB_DEVICE"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class OB_DEVICE_MAP(db.Model):
    __tablename__ = "OB_DEVICE_MAP"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class OB_GATEWAY(db.Model):
    __tablename__ = "OB_GATEWAY"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class OB_GATEWAY_MAP(db.Model):
    __tablename__ = "OB_GATEWAY_MAP"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class OB_RESOURCE(db.Model):
    __tablename__ = "OB_RESOURCE"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }

class CM_TIME(db.Model):
    __tablename__ = "CM_TIME"
    __table_args__ = { 'autoload' : True, 'autoload_with': db.engine }


''' TABLE-VIEW '''   
class VW_OB_OBJECTS(db.Model):
    __table__ = Table("VW_OB_OBJECTS"
                      , db.metadata,Column('ep_id',NVARCHAR(32),primary_key=True)
                      , autoload=True
                      , autoload_with=db.engine
                      , extend_existing=True )
    
class SCH_RM_ENDPOINT_DATA(ModelSchema):
    class Meta:
        model = RM_ENDPOINT_DATA
 
class SCH_OB_RESOURCE(ModelSchema): 
    class Meta: model = OB_RESOURCE

class SCH_OB_GATEWAY(ModelSchema):
    class Meta:
        model = OB_GATEWAY

class SCH_OB_DEVICE(ModelSchema):
    class Meta:
        model = OB_DEVICE

class SCH_OB_ENDPOINT(ModelSchema):
    class Meta:
        model = OB_ENDPOINT
'''
SqlAlchemyObjectSerializer
'''
rm_endpoint_data_many  = SCH_RM_ENDPOINT_DATA(many=True)        
ob_resource_many       = SCH_OB_RESOURCE(many=True)
ob_resource_single     = SCH_OB_RESOURCE(many=False)
ob_gateway_many        = SCH_OB_GATEWAY(many=True)
ob_gateway_single      = SCH_OB_GATEWAY(many=False)
ob_device_many         = SCH_OB_DEVICE(many=True)
ob_device_single       = SCH_OB_DEVICE(many=False)
ob_endpoint_many       = SCH_OB_ENDPOINT(many=True)
ob_endpoint_single     = SCH_OB_ENDPOINT(many=False)

if __name__ == '__main__':
    for x in db.session.query(OB_ENDPOINT).all():  # @UndefinedVariable
        print(x)