from django.urls import path
from ugiinbichig.views import HealthView

urlpatterns = [
    path('', HealthView.as_view(), name='health')
]