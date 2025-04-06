from django.urls import path
from ugiinbichig.views import PunishmentView

urlpatterns = [
    path('', PunishmentView.as_view(), name='death'),
] 