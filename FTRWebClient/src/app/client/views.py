from flask.views import View, MethodView
from flask.templating import render_template

from datetime import datetime 
from wtforms import Form,BooleanField, StringField, PasswordField, validators, IntegerField,SelectField,TextAreaField,DateField
from wtforms.validators import DataRequired, Required

class KAFKA_PRODUCER_FORM(Form):
    ep_id = StringField(u'엔드포인트id',[validators.required(), validators.Length(min=32,max=32)])
    ep_type = StringField(u'타입', [validators.required(),validators.Length(min=1,max=50)],render_kw={'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    ep_scale = StringField(u'스케일', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" })
    ep_value = StringField(u'값', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" }) 
    
class KAFKA_PRODUCER(MethodView):
    def get(self):
        form = KAFKA_PRODUCER_FORM()
        return render_template('client/kaf_prod.html',form=form)
    
    def post(self):
        pass