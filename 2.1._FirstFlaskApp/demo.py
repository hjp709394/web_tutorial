import argparse

from flask import Flask
app = Flask(__name__)

@app.route("/")
def HelloFlask():
        return "MengJiang is magnanimous"

