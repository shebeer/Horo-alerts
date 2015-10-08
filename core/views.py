from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import thread,threading
from django.core.mail import EmailMessage
from core.models import Prediction,Zodiac,UserProfile
import time
import datetime
from django.conf import settings

# Create your views here.
threadLock = threading.Lock()


def home(request):

    thread1 = Horoscope(1, "Thread-For-Horoscope")
    thread1.start()
    return render(request, 'core/home.html')


def horoscope():
    while True:
        alert_time = settings.ALERT_TIME
        now = datetime.datetime.now()
        curr_time = str(now.hour)+':'+str(now.minute)
        if curr_time == alert_time:
            date = time.strftime("%Y-%m-%d")
            if not Zodiac.objects.filter(date=date):
                soup = BeautifulSoup(requests.get("http://www.littleastro.com/").text, 'html.parser')
                date = soup.find('span').string
                content = soup.find('ul')
                horoscopes = content.find_all('li')
                zodiacs = {}
                array = []
                for signs in horoscopes:
                    sign = signs.h3.string.split()[1]
                    prediction = signs.find('p').string
                    zodiacs[sign] = prediction
                    object = Prediction(zodiac=sign, prediction=prediction)
                    object.save()
                    array.append(object)
                zod_object = Zodiac(date=date)
                zod_object.save()
                zod_object.zodiac.add(*array)
            send_alerts(date)


def send_alerts(date):
    objects = Zodiac.objects.filter(date=date)
    if objects:
        predictions = objects[0].zodiac
        prediction = predictions.filter(zodiac="Cancer")
        if prediction:
            zodiac = prediction[0].zodiac
            predict = prediction[0].prediction
            email = EmailMessage(zodiac, predict, to=['shabeersha33@gmail.com'])
            email.send()


class Horoscope (threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name

    def run(self):
        print "Starting " + self.name
        threadLock.acquire()
        horoscope()
        threadLock.release()
