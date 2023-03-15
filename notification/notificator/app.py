import logging

from build.config import settings
from build.utils.app_factory import create_app
from build import scheduler # <- Shedule starts here

app = create_app(settings)


# jwt = JWTManager(app)


@app.route("/")
def index():
    return "Hello to Flask!"


for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run()
