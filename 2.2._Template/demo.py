from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def HelloTemplate():
    return render_template('hello_template.html', message="MengJiang is friendly")

