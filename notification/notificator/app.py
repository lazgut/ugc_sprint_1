import logging

from build.utils.app_factory import create_app
from build.config import settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = create_app(settings)


# jwt = JWTManager(app)


@app.route("/")
def index():
    return "Hello to Flask!"


for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run()
