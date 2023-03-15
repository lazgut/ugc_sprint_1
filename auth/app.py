import logging

import logstash
from flask_jwt_extended import JWTManager

from config import settings
from utils.app_factory import create_app


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(
    logstash.LogstashHandler(settings.logstash_host, settings.logstash_port, version=1, tags='auth')
)


app = create_app(settings)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port)
