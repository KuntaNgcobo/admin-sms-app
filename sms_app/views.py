import time
from django.urls import reverse
import phonenumbers

from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import SMS


def index(request):
    sms_list = SMS.objects.order_by('date')[:5]
    context = {
        'sms_list': sms_list,
        }
    return render(request, 'index.html', context)

def sms_form(request):
    if request.method == "POST":
        return send_sms(request)

    context = {}
    return render(request, 'sms_form.html', context)

def send_sms(request):
    sms = {
        "time_now": datetime.now(),
        "status": "PENDING",
        }
    try:
        #selected_choice = question.choice_set.get(pk=request.POST['choice'])
        phone_number = phonenumbers.parse( request.POST['number'] )
        sms["number"] = phone_number
        sms["message"] = request.POST['message']

        print("Send start", sms)
        if not phonenumbers.is_valid_number_for_region(phone_number, "ZA"):
            raise KeyError
        
    except (KeyError):
        # Redisplay the question voting form.
        print("Error")
        return render(request, 'sms_form.html', {
            'number_error': "Number not valid for South Africa",
        })
    else:
        print("Else")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        time.sleep(1)
        return HttpResponseRedirect(reverse('sms_app:index'))
        return render(request, 'index.html', sms)
