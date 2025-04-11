from django.urls import path
from ugiinbichig.views.getHumanDetails import HumanDetails

urlpatterns = [
    path('', HumanDetails.as_view(), name='get_human_details'),
]
