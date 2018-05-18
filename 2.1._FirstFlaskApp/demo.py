from flask import Flask
app = Flask(__name__)

@app.route("/")
def HelloFlask():
    return "Meng-Jiang is magnanimous"

