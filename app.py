from flask import Flask, render_template, request
from flask_sock import Sock
from framework import store
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

sock = Sock(app)
sock.init_app(app)


@app.route("/")
def hello_world():
    return render_template(
        'index.html'
        )


@sock.route('/chat')
def echo(ws):
    from framework import FlaskCallbackHandler
    query = request.args.get("query")
    handler = FlaskCallbackHandler(ws)
    store.chat(query, [handler])
