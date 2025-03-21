from django.urls import path
from ugiinbichig.views import Relation

urlpatterns = [
    path('', Relation.as_view(), name='relation'),
]
