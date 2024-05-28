#!/usr/bin/python3
""" Get locale from request """
from config import Config
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
# app.url_map.strict_slashes = False
babel = Babel(
    app=app,
    default_locale=Config.LANGUAGES[0],
    default_timezone=Config.TIMEZONES[0]
)


@babel.localeselector
def get_locale():
    """ Get web app locale """
    languages = request.accept_languages
    return languages.best_match(Config.LANGUAGES)


@app.route("/")
def home():
    """ Display content from html files for the route """
    return render_template("1-index.html")


if __name__ == "__main__":
    """ Main Function """
    app.run(debug=True)
