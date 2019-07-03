from django.http import HttpResponse
from django.shortcuts import render
import json

from stone.stone_log_utls import *

from django.forms.models import model_to_dict


from core.models import BackResult

# Create your views here.


def test_logger(request):
    info_logger.debug('This is a log from customize logger debug')
    info_logger.info('This is a log from customize logger info')
    return HttpResponse("Nothing to show")


def chart(request, record_id):
    br = BackResult.objects.get(pk=record_id)
    res = model_to_dict(br)
    return render(request, 'chart_by_record.html', res)
