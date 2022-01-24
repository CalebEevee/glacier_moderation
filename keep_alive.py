from threading import Thread

from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "Your bot is alive!\nThis is the webserver for Glacier Moderation!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()


keep_alive()
