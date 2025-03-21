from django.urls import path
from ugiinbichig.views import HumanView,  ShapeList

urlpatterns = [
    path('', HumanView.as_view(), name='human'),
    path('shape/', ShapeList.as_view(), name='shape'),
]
