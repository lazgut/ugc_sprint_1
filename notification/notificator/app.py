from flask import Flask

from .src.event_action import event_page

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello to Flask!'


app.register_blueprint(event_page)


# main driver function
if __name__ == "__main__":
    app.run()
