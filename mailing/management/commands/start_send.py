from django.core.management import BaseCommand

from mailing.services import start


class Command(BaseCommand):
    """Команда на запуск рассылки"""

    def handle(self, *args, **options):

        start()
