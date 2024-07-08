from secrets import token_urlsafe
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.validators import DataRequired


class NamerForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    email = StringField('What is your email', validators=[DataRequired()])
    hidden_field = HiddenField('Hidden Field')
    location = StringField('What is your location')
    submit = SubmitField('Submit')


class TradeForm(FlaskForm):
    ticker = StringField('Ticker')
    submit = SubmitField()
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')