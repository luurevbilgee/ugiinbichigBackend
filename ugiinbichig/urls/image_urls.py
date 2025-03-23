from django.urls import path
from ugiinbichig.views import UserImage
urlpatterns = [
    path('', UserImage.as_view(), name='image')
]
