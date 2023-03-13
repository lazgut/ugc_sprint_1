import os
import smtplib
from email.message import EmailMessage
from http import HTTPStatus

from jinja2 import Environment, FileSystemLoader

from build.config import settings


class EmailSender:
    @classmethod
    def send_mail(cls,
                  destination: list,
                  subject: str,
                  html_template: str,
                  title: str,
                  text: str,
                  image: str = ""
                  ) -> (str, HTTPStatus):  # type: ignore
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(settings.email_user, settings.email_password)

        message = EmailMessage()
        message["From"] = settings.email_user
        message["To"] = destination
        message["Subject"] = subject

        path = f'{os.path.dirname(__file__)}/html_template'

        env = Environment(loader=FileSystemLoader(path))  # расположение шаблонов
        template = env.get_template(html_template)  # Загружаем нужный шаблон в переменную
        output = template.render(**{
            'title': title,
            'text': text,
            'image': image
        })
        message.add_alternative(output, subtype='html')
        server.sendmail(settings.email_user, destination, message.as_string())
        server.close()
        return "Success", HTTPStatus.OK
