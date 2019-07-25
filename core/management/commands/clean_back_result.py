# coding:utf-8

from django.core.management import BaseCommand

from command_utils import iterate_for_all
from core.models import BackResult


class Command(BaseCommand):
    def handle(self, *args, **options):
        objs = iterate_for_all(BackResult, True)
        for obj in objs:
            obj.delete()
