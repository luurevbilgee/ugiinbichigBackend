from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Login, Signup, CreateTokenView, UserView, CheckTokenView

urlpatterns =[
    path('login/', Login.as_view(), name= 'login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('auth/token/',CreateTokenView.as_view(), name='token_create'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/check/', CheckTokenView.as_view(), name  ='check_token')
]

if settings.DEBUG:  # Хөгжүүлэлтийн үед л ажиллана
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)