from django.core.management.base import BaseCommand
from purifier.utils import run_scheduler

class Command(BaseCommand):
    help = 'Run the scheduler'

    def handle(self, *args, **kwargs):
        run_scheduler()