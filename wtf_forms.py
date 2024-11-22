from secrets import token_urlsafe
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField
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
    
class DropdownForm(FlaskForm):
    # Dropdown field
    options = SelectField(
        'Choose a database',
        choices=[
            (False, 'Create a new database'),
            ('option2', 'Option 2'),
            ('option3', 'Option 3'),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField('Submit')


class DropdownForm2(FlaskForm):
    options = SelectField('Choose a database', validators=[DataRequired()])
    submit = SubmitField('Submit')