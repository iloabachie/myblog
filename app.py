from flask import Flask, render_template
from os import getenv



# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('index.html', name=name)



if __name__ == "__main__":
    if getenv('FLASK_ENV') == 'development':
        app.run(debug=True) # for dev testing
    else:
        app.run() # For production