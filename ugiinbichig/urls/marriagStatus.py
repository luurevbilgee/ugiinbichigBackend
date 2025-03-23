from django.urls import path
from ugiinbichig.views import DivorceView, MarryView

urlpatterns = [
    path('divorce/', DivorceView.as_view(), name='divorce'),
    path('marry/' , MarryView.as_view(), name='marry')
]