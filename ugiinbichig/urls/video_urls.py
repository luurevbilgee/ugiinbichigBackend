from django.urls import path
from ugiinbichig.views import  VideoView
urlpatterns = [
    path('', VideoView.as_view(), name='video')
]
