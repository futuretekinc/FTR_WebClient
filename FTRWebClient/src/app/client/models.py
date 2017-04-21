 
from app import db

class RM_ENDPOINT_DATA(db.Model):
    __tablename__ = "RM_ENDPOINT_DATA"
    __table_args__ = {
        'autoload' : True,
#         'schema' : 'appdb',
        'autoload_with': db.engine
    }
    
if __name__ == '__main__':
    rows = db.session.query(RM_ENDPOINT_DATA).all()  # @UndefinedVariable
    for x in rows:
        print(x)
#     