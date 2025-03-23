from django.urls import path
from ugiinbichig.views import DeathView

urlpatterns = [
    path('', DeathView.as_view(), name='death'),
]