from flask import Blueprint, request
from .senders.email import EmailSender

V1 = "/v1"
event_page = Blueprint('event_page', __name__, url_prefix=V1)


@event_page.route('/api/on_event', methods=['POST'])
def on_event():
    # TODO Place some dispatching code here, "if .... :",
    # refer to request.data.
    if True:
        #  DATA FOR DEBUG
        destination = ["yp.group10@yandex.ru", "kaysaki@yandex.ru"]
        subject = "Привет!"
        html_template = 'mail.html'
        title = 'Новое письмо!'
        text = 'Произошло что-то интересное! :)'
        image = 'https://upload.wikimedia.org/wikipedia/ru/4/4d/Wojak.png'

        EmailSender.send_mail(destination, subject, html_template, title, text, image)
    return f"route works, data: {request.data}"
