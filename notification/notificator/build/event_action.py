from flask import Blueprint, request

from .resources.parsers.event_action import manual_sender_parser
from .senders.email import EmailSender

V1 = "/v1"
event_page = Blueprint('event_page', __name__, url_prefix=V1)


@event_page.route('/manual_sender', methods=['POST'])
def on_event():
    data = manual_sender_parser.parse_args()
    payload, status = EmailSender.send_mail(data['destination'],
                                            data['subject'],
                                            data['html_template'],
                                            data['title'],
                                            data['text'],
                                            data['image'])
    return payload, status
