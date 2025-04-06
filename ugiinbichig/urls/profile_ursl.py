from django.urls import path
from ugiinbichig.views import ProfilePictureView

urlpatterns = [
    path('', ProfilePictureView.as_view(), name='profile_picture')
]
