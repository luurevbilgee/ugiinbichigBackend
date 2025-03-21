from django.urls import path
from ugiinbichig.views import UserNamtarView

urlpatterns = [
    path('namtar/', UserNamtarView.as_view(), name='user_namtar'),
]
