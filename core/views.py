from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
from django.core.mail import EmailMessage
from core.models import Prediction, Zodiac, UserProfile
from core.utils import is_dob_between
from .horoscope_signs import *
from django.conf import settings
from django.contrib.auth.models import User
import json
import traceback
import requests
import thread, threading
import time
import datetime
import logging
logger = logging.getLogger('horoscope')
# Create your views here.
# threadLock = threading.Lock()

def get_sign_from_date(dob):

    if dob >= capricon_start or dob <= capricon_end:
        return 'capricorn'
    if is_dob_between(dob,aries_start,aries_end):
        return 'aries'
    if is_dob_between(dob,taurus_start,taurus_end):
        return 'taurus'
    if is_dob_between(dob,gemini_start,gemini_end):
        return 'gemini'
    if is_dob_between(dob,cancer_start,cancer_end):
        return 'cancer'
    if is_dob_between(dob,leo_start,leo_end):
        return 'leo'
    if is_dob_between(dob,virgo_start,virgo_end):
        return 'virgo'
    if is_dob_between(dob,libra_start,libra_end):
        return 'libra'
    if is_dob_between(dob,scorpio_start,scorpio_end):
        return 'scorpio'
    if is_dob_between(dob,sagittarius_start,sagittarius_end):
        return 'sagittarius'
    if is_dob_between(dob,aquarius_start,aquarius_end):
        return 'aquarius'
    if is_dob_between(dob,pisces_start,pisces_end):
        return 'pisces'
    return "Couldn't find!"

def home(request):
    try:
        # thread1 = Horoscope(1, "Thread-For-Horoscope")
        # thread1.start()
        logger.debug('Horoscope home page request recieved')
        today = datetime.datetime.now()
        print today
        zodiacs = Zodiac.objects.filter(date=today)
        now = datetime.datetime.now()
        curr_time = str(now.hour)+':'+str(now.minute)
        predictions = 'None'
        print zodiacs
        if not zodiacs:
            print 'current_time',curr_time
            if curr_time > '12:00': #Only after 12 will get updated content
                fetch_horoscope_of_date(today)
            else:
                today = yesterday = datetime.datetime.mnow() - datetime.timedelta(hours=24)
            zodiacs = Zodiac.objects.filter(date=today)
        if zodiacs:
            predictions =  zodiacs[0].zodiac.all()
        else:
            predictions = []
        context = {
            'predictions' : predictions,
            'today' :today,
        }
        return render(request, 'core/index.html',context)
    except Exception as e:
        logger.error(traceback.format_exc())
        return render(request, 'core/index.html',{})

def fetch_horoscope_of_date(date):
    try:
        if not Zodiac.objects.filter(date=date):
            logger.debug('Fetching horoscope for date %s'%(str(date)))
            soup = BeautifulSoup(requests.get("http://www.littleastro.com/").text, 'html.parser')
            content = soup.find('ul')
            horoscopes = content.find_all('li')
            zodiacs = {}
            array = []
            for signs in horoscopes:
                sign = signs.h3.string.split()[1]
                logger.debug('sign fetched for date %s '%str(date))
                prediction = signs.find('p').string
                zodiacs[sign] = prediction
                object = Prediction(zodiac=sign, prediction=prediction)
                object.save()
                array.append(object)
            zod_object = Zodiac(date=date)
            zod_object.save()
            zod_object.zodiac.add(*array)
    except Exception as e:
        logger.error('Exception at fetch horscope_of_date : %s , message:%s'%(str(date),str(e)))

def send_alerts(date):
    try:
        objects = Zodiac.objects.filter(date=date)
        users = UserProfile.objects.all()
        predictions = objects[0].zodiac
        for x in users:
            prediction = predictions.filter(zodiac=x.zodiac)
            if prediction:
                zodiac = prediction[0].zodiac
                predict = prediction[0].prediction
                email = EmailMessage(zodiac, predict, to=[x.user.email])
                email.send()
    except Exception as e:
        logger.error(traceback.format_exc())

def subscribe(request):
    try:
        data = request.POST
        if request.method == 'POST':
            if not User.objects.filter(email=data['email']):
                user_obj = User(username=data['email'],
                                    first_name=data['name'],
                                    email=data['email'])
                user_obj.save()
                dob_tuple = (int(data['dob'].split('/')[1]),int(data['dob'].split('/')[0]))
                dob = datetime.datetime.strptime(data['dob'], '%d/%m/%Y')
                zodiac = get_sign_from_date(dob_tuple)
                user_prof_obj = UserProfile(user=user_obj,zodiac=zodiac,dob=dob)
                user_prof_obj.save()

                today = time.strftime("%Y-%m-%d")
                zodiacs = Zodiac.objects.filter(date=today)
                prediction = 'None'
                if zodiacs:
                    predictions =  zodiacs[0].zodiac.filter(zodiac__iexact=zodiac)
                    if predictions:
                        prediction = predictions[0].prediction
                context = {
                    'zodiac' : zodiac,
                    'prediction' : prediction,
                    'today' :datetime.datetime.now(),
                    'status' : True
                }
            else:
                context = {
                    'status' : False
                }

            return render(request,'core/success.html',context)
        else:
            return HttpResponseRedirect('/')
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponseRedirect('/')

def custom_404(request):
    return render(request,'core/404.html')

# def fetch_horoscope(request):
#     date = time.strftime("%Y-%m-%d")
#     thread.start_new_thread(fetch_horoscope_of_date,(date,))
#     return render(request,'core/404.html')

#     while True:
#         alert_time = settings.ALERT_TIME
#         now = datetime.datetime.now()
#         curr_time = str(now.hour)+':'+str(now.minute)
#         if curr_time == alert_time:
#             date = time.strftime("%Y-%m-%d")
#             fetch_horoscope_of_date(date)
#             send_alerts(date)

# class Horoscope (threading.Thread):
#     def __init__(self, thread_id, name):
#         threading.Thread.__init__(self)
#         self.threadID = thread_id
#         self.name = name
#
#     def run(self):
#         print "Starting " + self.name
#         threadLock.acquire()
#         horoscope()
#         threadLock.release()

# def to_days_horoscope(request,zodiac):
#     today = time.strftime("%Y-%m-%d")
#     zodiacs = Zodiac.objects.filter(date=today)
#     prediction = 'None'
#     if zodiacs:
#         predictions =  zodiacs[0].zodiac.filter(zodiac__iexact=zodiac)
#         if predictions:
#             prediction = predictions[0].prediction
#     context = {
#         'zodiac' : zodiac,
#         'prediction' : prediction,
#         'today' :datetime.datetime.now(),
#     }
#     return render(request,'core/subscribed.html',context)

