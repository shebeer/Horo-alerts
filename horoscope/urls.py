from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    url(r'^subscribe/$', 'core.views.subscribe', name='subscribe'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^get/horoscope/([a-zA-Z]+)/$', 'core.views.to_days_horoscope', name='today_horoscope'),
    # url(r'^get/horoscope/of/today/$', 'core.views.fetch_horoscope', name='fetch_horoscope'),
]

handler404 = 'core.views.custom_404'
