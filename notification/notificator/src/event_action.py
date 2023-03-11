from flask import Blueprint, request
from .senders.email import EmailSender
event_page = Blueprint('event_page', __name__)


@event_page.route('/api/v1/on_event', methods=['POST'])
def on_event():
    # TODO Place some dispatching code here, "if .... :",
    # refer to request.data.
    if True:
        EmailSender.send()
    return f"route works, data: {request.data}"
