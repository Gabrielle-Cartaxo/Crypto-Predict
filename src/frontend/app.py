import os
from flask import Flask, render_template
from urllib.parse import quote as url_quote


app = Flask(__name__, 
            static_folder='static', 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
