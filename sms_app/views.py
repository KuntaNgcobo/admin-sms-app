from django.http import HttpResponse
from django.shortcuts import render

from .models import SMS

def index(request):
    sms_list = SMS.objects.order_by('date')[:5]
    context = {
        'sms_list': sms_list,
        }
    return render(request, 'index.html', context)
