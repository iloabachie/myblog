from os import getenv
import csv
from flask import Flask, render_template, flash, request, redirect, send_from_directory
from secrets import token_urlsafe
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
import mysql.connector
from trading.trade_analysis import trade_analysis


# create MySQL database
# def create_and_verify_db(db_name, user='root', host='localhost', passwd="3984", port=3306):
def create_and_verify_db(db_name, user=getenv('DBUSER'), host=getenv('DBHOST'), passwd=getenv('DBPASSWD'), port=3306):
    mydb = mysql.connector.connect(host=host, user=user, passwd=passwd, port=port)
    my_cursor = mydb.cursor()    
    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        if db[0] == db_name:
            break
    else:
        my_cursor.execute(f"CREATE DATABASE {db_name}")        

# create_and_verify_db('users_database', port=3307)
create_and_verify_db('user_database')

# Create a Flask Instance
app = Flask(__name__)
per_page = 7
app.secret_key = "random secret" # token_urlsafe(16)
csrf = CSRFProtect(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:3984@localhost:3307/users_database"
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('MYSQLDB') 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(120))
    
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
    location = StringField('What is your location')
    submit = SubmitField('Submit')
    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.context_processor
def inject_defaults():
    default_year = date.today()
    company_name = "MyBlog"
    return dict(default_year=default_year, company_name=company_name)

@app.route('/')
def index():
    with open(getenv('LOG_FILE'), 'a') as file:
        visitor_ip = request.remote_addr
        file.write(f"Home Page:    {visitor_ip} - {datetime.utcnow()}\n")
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
            user = Users(name=form.name.data, email=form.email.data, location=form.location.data)
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            # user_list = Users.query.order_by(Users.date_added)
            flash("User added successfully!!!")
        else:
            user_exists = True
        form.name.data = ''
        form.email.data = ''  
        form.location.data = ''  
    user_list = Users.query.order_by(Users.date_added)
    all_users = []
    for user in user_list:
        all_users.append(user)
    page = request.args.get('page', 1, type=int)
    # per_page = 5
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
    # per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(all_users) + per_page - 1) // per_page
    items_on_page = all_users[start:end]
        
    form = NamerForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.location = request.form['location']
        try:
            db.session.commit()
            flash("User updated successfully")
            form.name.data = ''
            form.email.data = '' 
            form.location.data = '' 
            return render_template('add_user.html', name=None, user_exists=None, form=form, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)
        except Exception as e:
            flash("Error in update. Try again")
            return render_template("update.html", form=form, name_to_update=name_to_update, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)
    else:
        return render_template("update.html", form=form, id=id, name_to_update=name_to_update, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None   
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully !!!")
        form = NamerForm()  
        user_list = Users.query.order_by(Users.date_added)
        all_users = []
        for user in user_list:
            all_users.append(user)
        page = request.args.get('page', 1, type=int)
        # per_page = 5
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(all_users) + per_page - 1) // per_page
        items_on_page = all_users[start:end]
        return render_template("add_user.html", form=form, name=name, user_list=user_list, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)
    except Exception as e:
        print(e)
        flash(f"Error in deletion: {e}")
        name = None
        user_exists = False
        form = NamerForm()  
        user_list = Users.query.order_by(Users.date_added)
        all_users = []
        for user in user_list:
            all_users.append(user)
        page = request.args.get('page', 1, type=int)
        # per_page = 5
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(all_users) + per_page - 1) // per_page
        items_on_page = all_users[start:end]
        return render_template('add_user.html', name=name, form=form, user_list=user_list, user_exists=user_exists, all_users=all_users, items_on_page=items_on_page, page=page, total_pages=total_pages)

@app.route('/trading/download_txt')
def download():
    return send_from_directory('downloads', path="recommendation.txt", as_attachment=True)

@app.route('/trading/download_csv')
def download_csv():
    return send_from_directory('downloads', path="recommendation.csv", as_attachment=True)

class TradeForm(FlaskForm):
    ticker = StringField('Ticker')
    submit = SubmitField()
    
@app.route('/trading', methods=['POST', 'GET'])
def recommendations():
    with open(getenv('LOG_FILE'), 'a') as file:
        visitor_ip = request.remote_addr
        file.write(f"Trading Page: {visitor_ip} - {datetime.utcnow()}\n")
    form = TradeForm()
    if request.method == 'POST':
        # ticker = request.form.get('ticker')
        ticker = form.ticker.data
        analysis = trade_analysis(ticker)
        time_stamp = str(datetime.utcnow())
        intervals = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1W', '1M']
        columns = ['RECOMMENDATION', 'BUY', 'SELL', 'NEUTRAL']
        with open(f"./downloads/{ticker} {time_stamp.replace(':', '.')}.txt", 'w') as file:
            file.write("Trading recommendation for " + ticker[:3] + '/' + ticker[3:] + '\n')
            file.write('Time Stamp (UTC): ' + time_stamp + '\n')
            file.write(("+" + "=" * 16) * 5 + "+\n")            
            file.write(f"| {'INTERVAL':14} ")
            for col in columns:
                file.write(f'| {col:14} ')
            file.write('|\n')
            file.write(("+" + "=" * 16) * 5 + "+\n")
            for interval in intervals:
                file.write(f'| {interval:14} ')
                for col in columns:
                    file.write(f'| {str(analysis[interval][col]):14} ')
                file.write('|\n')
                file.write(("+" + "-" * 16) * 5 + "+\n")  
        with open(f"./downloads/{ticker} {time_stamp.replace(':', '.')}.csv", 'w', newline="\n") as file:
            writer = csv.writer(file)
            writer.writerow(['INTERVAL', 'DATE', 'TIME'] + columns)
            date = time_stamp[:10]
            time = time_stamp[11:19]
            for interval in intervals:
                writer.writerow([interval, date, time] + [str(analysis[interval][col]) for col in columns])
            
        return render_template('trade/recommendation.html', form=form, ticker=ticker, time_stamp=time_stamp, analysis=analysis)
    return render_template('trade/recommendation.html', form=form)

@app.route('/widget')
def widget():
    return render_template('trade/widget.html')


if __name__ == "__main__":
    if getenv('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', debug=True, port=5000)
    else:
        app.run()
        