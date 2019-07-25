from django.core.management import BaseCommand

from core.models import BackResultYear


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(0, 360608):
            print i
            try:
                obj = BackResultYear.objects.get(pk=i)
                obj.param_string = obj.param_string.replace(' ', '_').replace(':', '_')
                obj.save()
            except:
                pass
