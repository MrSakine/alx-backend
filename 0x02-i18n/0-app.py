#!/usr/bin/python3
""" Basic Flask app """
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def home():
    """ Display content from html files for the route """
    return render_template("0-index.html")


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)