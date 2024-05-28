#!/usr/bin/python3
""" Basic Babel setup """
from config import Config
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
# app.url_map.strict_slashes = False
babel = Babel(
    app=app,
    default_locale=Config.LANGUAGES[0],
    default_timezone=Config.TIMEZONES[0]
)


@app.route("/")
def home():
    """ Display content from html files for the route """
    return render_template("1-index.html")


if __name__ == "__main__":
    """ Main Function """
    # babel.init_app(app)
    app.run(debug=True)
