from django.conf.urls import url
from . import views

app_name = 'usuarios'

urlpatterns = [
    url(r'^register/', views.RegistroUsuario.as_view(), name="register"),
]