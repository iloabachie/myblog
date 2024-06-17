from os import getenv
from flask import Flask, render_template, flash, request
from secrets import token_urlsafe
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector
import sys
sys.path.insert(0, "D:/Documents/Python lessons/myblog/venv/Lib/site-packages") # identify location of pymysql


# create MySQL database
def create_and_verify_db(db_name, user='root', host='localhost', passwd="P@s$w0rd1$", port=3306):
    mydb = mysql.connector.connect(host=host, user=user, passwd=passwd, port=port)
    my_cursor = mydb.cursor()    
    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        if db[0] == db_name:
            break
    else:
        my_cursor.execute(f"CREATE DATABASE {db_name}")        

create_and_verify_db('users_database', port=3307)

# Create a Flask Instance
app = Flask(__name__)

app.secret_key = "qwerty" #token_urlsafe(16)
csrf = CSRFProtect(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:P%40s$w0rd1$@localhost:3307/users_database"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlclient://root:P%40s$w0rd1$@localhost:3307/users_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'{self.name}'

# Create a function to create the database tables for sqllite
def create_table():
    with app.app_context():        
        db.create_all()

# Example: Run the create_tables function when the script is executed
if __name__ == '__main__':
    create_table()

class NamerForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    email = StringField('What is your email', validators=[DataRequired()])
    hidden_field = HiddenField('Hidden Field')
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
        form.email.data = '' 
        flash("Form Submitted Successfully!!!")
    return render_template('name.html', name=name, form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = email = user_list = None
    user_exists = False
    form = NamerForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            # user_list = Users.query.order_by(Users.date_added)  
            flash("User added successfully!!!")  
        else:
            user_exists = True
        form.name.data = ''
        form.email.data = ''  
    user_list = Users.query.order_by(Users.date_added)
    all_users = []
    for user in user_list:
        all_users.append(user)
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(all_users) + per_page - 1) // per_page
    items_on_page = all_users[start:end]
        
    return render_template('add_user.html', name=name, form=form, user_list=user_list, user_exists=user_exists, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_list = Users.query.order_by(Users.date_added)
    all_users = []
    for user in user_list:
        all_users.append(user)
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(all_users) + per_page - 1) // per_page
    items_on_page = all_users[start:end]
        
    form = NamerForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            print("did you run?")
            flash("User updated successfully")
            return render_template('add_user.html', name=None, user_exists=None, form=form, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)
        except:
            print('error in rendering when update failed')
            # if error not tested
            flash("Error in update. Try again")
            return render_template("update.html", form=form, name_to_update=name_to_update, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)
    else:
        # OK
        print('page to render once route called via link')
        return render_template("update.html", form=form, name_to_update=name_to_update, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)



if __name__ == "__main__":
    if getenv('FLASK_ENV') == 'development':
        app.run(debug=True) # for dev testing
    else:
        app.run(host='0.0.0.0', port=5000) # For production
        