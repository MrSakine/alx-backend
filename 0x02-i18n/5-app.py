#!/usr/bin/env python3
""" Get locale from request """
from flask import Flask, g, render_template, request
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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """ Retrieves the locale for a web page """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    Returns a user dictionary or None if the ID cannot be found
    or if login_as was not passed
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.route("/")
def home():
    """ Display content from html files for the route """
    return render_template("5-index.html")


@app.before_request
def before_request():
    """ before_request method """
    g.user = get_user()


if __name__ == "__main__":
    app.run()
