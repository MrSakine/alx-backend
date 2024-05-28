#!/usr/bin/python3
""" Get locale from request """
from config import Config
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """ Config class definition """
    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ Get web app locale """
    languages = request.accept_languages
    config = app.config['LANGUAGES']
    return languages.best_match(config)


@app.route("/")
def home():
    """ Display content from html files for the route """
    return render_template("2-index.html")


if __name__ == "__main__":
    """ Main Function """
    app.run(debug=True)
