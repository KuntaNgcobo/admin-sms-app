from datetime import datetime
from requests import RequestException

from django.contrib.auth import views
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from .models import Message

import phonenumbers
import os

from dotenv import dotenv_values

#envvar = dotenv_values(".env")
#client = Client(envvar["TA_SID"], envvar["TA_TOKEN"])
client = Client(os.environ.get('EMAIL_HOST_USER'), os.environ.get('EMAIL_HOST_USER'))

def authenticate(request):
    print("AUTH:",request.user,request.user.is_authenticated, request.user.is_anonymous)
    if not request.user.is_authenticated or request.user.is_anonymous:
        context = {
                "error": "There Was An Error Logging In, Try Again...",
                "html": views.LoginView.form_class(),
            }
        return render(request, 'login.html', context)

def index(request):
    authenticate(request)
    reload_status()

    sms_list = Message.objects.order_by('date')[::-1]
    context = {
        'sms_list': sms_list[:8],
        }
    return render(request, 'index.html', context)

def reload_status():
    queued = Message.objects.filter( status="queued" )
    queued_sids = [ msg.sms_id for msg in queued ]

    for sid in queued_sids:
        try:            
            message_status = client.messages.get(sid).fetch().status
            message = Message.objects.filter( sms_id = sid )
            for msg in message:
                msg.status = message_status
                msg.save()

        except TwilioRestException:
            print( f"Message with sid {sid} failed to obtain status" )

        except RequestException:
            print( f"Network request failure" )

def sms_form(request):
    authenticate(request)
    if request.method == "POST":
        return send_sms(request)

    return render(request, 'sms_form.html', {})

def number_message_check(number, message):
    parsed_phone_number = phonenumbers.parse( number )
    if not message or not number:
        raise ValueError("Please enter a message or a number.")
    elif len( message ) > 160:
        raise ValueError("Message to long, keep it under 160 characters.")
    elif not phonenumbers.is_valid_number_for_region(parsed_phone_number, "ZA"):
        raise phonenumbers.NumberParseException

    return parsed_phone_number

def send_sms(request):
    print("req", request)
    sms = {
        "message": request.POST['message'], 
        "number": request.POST['number'],
        }
    try:
        parsed_phone_number = number_message_check( sms["number"], sms["message"] )

    except ValueError as e:
        print("############################################################")
        return render(request, 'sms_form.html', {
            'message_error': e,
        })

    except phonenumbers.NumberParseException:
        print("############################################################")
        return render(request, 'sms_form.html', {
            'number_error': "Number not valid",
        })

    else:
        sms["parsed_phone_number"] = parsed_phone_number

    try:
        print("Sending SMS...")
        message = client.messages.create(
                    body=sms["message"],
                    from_='+15076291974',
                    to=sms["number"], 
                    provide_feedback=True,
                )

    except RequestException as e:
        return render(request, 'sms_form.html', {
            'network_error': "Network Error Request Failed.",
        })
    except TwilioRestException as e:
        return render(request, 'sms_form.html', {
            'number_error': "Number is unverified.",
        })
    else:
        sms_sql = Message( sms_id = message.sid, number = sms["parsed_phone_number"], 
                message = sms["message"], status=message.status, date=datetime.now() )
        sms_sql.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('sms_app:index'))