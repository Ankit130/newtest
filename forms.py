from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField,DateTimeField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo,Required
from wtforms.fields.html5 import DateField
#from flask.ext.admin.form import widgets
#from wtforms_components import TimeField


class Emailpass(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TurnOnOff(FlaskForm):
	on_or_off = RadioField('Accept Job automatically', choices=[(1,'ON'),(0,'OFF'),(-1,'ON selected times')])
	submit = SubmitField('Submit')

class TimeFrame(FlaskForm):
    dt1 = DateTimeLocalField('Start Date')
    dt2 = DateTimeLocalField('start')
    


