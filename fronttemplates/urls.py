from django.conf.urls import url
from fronttemplates.views import *


app_name = 'fronttemplates'
urlpatterns = [
    url(r'^$', IndexView.as_view())
]