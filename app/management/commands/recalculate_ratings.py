from django.core.management.base import BaseCommand
import app.utils


class Command(BaseCommand):
    help = """This crank should give rating attributes of your tables some refresh!"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        app.utils.recalculateRating()
