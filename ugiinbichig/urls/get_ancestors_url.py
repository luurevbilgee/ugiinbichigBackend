from django.urls import path
from ugiinbichig.views.getAncester import AncestorsView

urlpatterns = [
    path('', AncestorsView.as_view(), name='get_ancestors'),
]
