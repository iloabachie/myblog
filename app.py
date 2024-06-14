from os import getenv
from flask import Flask, render_template
from secrets import token_urlsafe
# from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__)

foo = token_urlsafe(16)
app.secret_key = foo

# bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

# app.config['SECRET_KEY'] = foo 
class NamerForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Create a route decorator
@app.route('/')
def index():
    pizza = ['asss', 'bdddd', 'cffff', 'dggggg']
    return render_template('index.html', pizza=pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('name.html', name=name, form=form)











if __name__ == "__main__":
    if getenv('FLASK_ENV') == 'development':
        app.run(debug=True) # for dev testing
    else:
        app.run() # For production