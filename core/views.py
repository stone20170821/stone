from django.http import HttpResponse
from django.shortcuts import render

from stone.stone_log_utls import *


# Create your views here.


def test_logger(request):
    info_logger.debug('This is a log from customize logger debug')
    info_logger.info('This is a log from customize logger info')
    return HttpResponse("Nothing to show")
