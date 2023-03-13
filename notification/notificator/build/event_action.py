import logging
from flask import Blueprint, request
from .senders.email import EmailSender
from .db.helper import db_helper


V1 = "/v1"
event_page = Blueprint('event_page', __name__, url_prefix=V1)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@event_page.route('/on_event', methods=['POST'])
def on_event():
    # TODO Place some dispatching code here, "if .... :",
    # refer to request.data.
    payload = request.json["payload"]
    notification_event_pattern = db_helper.choose_event_pattern(payload["event_type"])
    new_notification_event = db_helper.add_notification_event(
        request.json["message_id"],
        notification_event_pattern["id"])
    if True:
        #  DATA FOR DEBUG
        destination = ["yp.group10@yandex.ru"]#, "kaysaki@yandex.ru"]
        subject = "Привет!"
        html_template = 'mail.html'
        title = 'Новое письмо!'
        text = 'Произошло что-то интересное! :)'
        image = 'https://upload.wikimedia.org/wikipedia/ru/4/4d/Wojak.png'

        EmailSender.send_mail(destination, subject, html_template, title, text, image)
    logger.info(f"route works, data: %s", request.data)
    return f"route works, data: {request.data}"

