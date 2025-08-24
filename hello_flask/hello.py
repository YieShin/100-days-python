from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"


def make_bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def make_emphasis(func):
    def wrapper(*args, **kwargs):
        return f"<em>{func(*args, **kwargs)}</em>"

    return wrapper


def make_underlined(func):
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"

    return wrapper


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye!"


if __name__ == "__main__":
    app.run(debug=True)

