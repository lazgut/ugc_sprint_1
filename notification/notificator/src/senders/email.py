import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
class EmailSender:
    @classmethod
    def send(self):
        logger.info("Place sending code here")