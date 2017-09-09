from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^login',views.login),
    url(r'^register',views.register),
    url(r'^sos', views.Sos.as_view()),
    url(r'^userregister', views.UserRegister.as_view()),
    url(r'^userlogin', views.UserLogin.as_view()),
    url(r'^locationupdate', views.LocationUpdate.as_view()),
    url(r'^requestotp', views.RequestOtp.as_view()),
    url(r'^message', views.Message.as_view()),
    url(r'^sos', views.Sos.as_view()),
    url(r'^', views.home),
]