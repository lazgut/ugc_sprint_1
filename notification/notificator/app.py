import logging

from src.utils.app_factory import create_app
from config import settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = create_app(settings)


# jwt = JWTManager(app)

@app.route('/')
def index():
    return 'Hello to Flask!'


if __name__ == "__main__":
    app.run()
