from flask import Flask, render_template
from os import getenv



# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')
def index():
    return '<details> \
        <summary>hello world</summary> \
        <p>hi</> \
        </details> \
        <details> \
        <summary>hello world</summary> \
        <p>hi</> \
        </details> \
        <details> \
        <summary>hello world</summary> \
        <p>hi</> \
        </details>'



if __name__ == "__main__":
    if getenv('FLASK_ENV') == 'development':
        app.run(debug=True) # for dev testing
    else:
        app.run() # For production