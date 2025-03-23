from django.urls import path
from ugiinbichig.views import SchoolView, MergejilView

urlpatterns = [
    path('school/', SchoolView.as_view(), name='school'),
    path('profession/', MergejilView.as_view(), name='mergejil'),
]