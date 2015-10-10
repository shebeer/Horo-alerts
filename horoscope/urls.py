from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    url(r'^subscribe/$', 'core.views.subscribe', name='subscribe'),
    url(r'^get_horoscope/([a-zA-Z]+)/$', 'core.views.to_days_horoscope', name='today_horoscope'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
