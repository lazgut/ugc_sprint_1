import logging
from typing import Iterable

from build.senders.email import EmailSender

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_all(users: Iterable[dict], patterns):
    """Send to all channels - email, telegram and so on."""
    for pattern in patterns:
        for user in users:
            send_email(user, pattern)


def send_email(user: dict, pattern):
    """
    Sample notification_pattern row:
    type_: 2
    pattern_file: mail.html
    actual_time: 600
    settings_: {"subject": "Привет", "title": "Новое письмо!", "text": "Произошло что-то интересное! :)",
        "image": "https://upload.wikimedia.org/wikipedia/ru/4/4d/Wojak.png"}
    """
    addresses = user["email"]
    file_pattern = pattern["pattern_file"]
    settings_ = pattern["settings_"]
    EmailSender.send_mail(addresses, settings_["subject"], file_pattern, settings_["title"],
                          settings_["text"], settings_["image"])
    logger.info(f"Sent to {addresses}, {file_pattern}, {settings_}")