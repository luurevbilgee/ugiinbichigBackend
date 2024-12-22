from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Login, Signup, CreateTokenView, UserView, CheckTokenView, HumanView, UserNamtarView, UserImage, ShapeList

urlpatterns =[
    path('login/', Login.as_view(), name= 'login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('auth/token/',CreateTokenView.as_view(), name='token_create'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/check/', CheckTokenView.as_view(), name  ='check_token'),
    path('human/', HumanView.as_view(), name ="human"),
    path('user/namtar', UserNamtarView.as_view(), name ="user_namtar"),
    path('namtar/', UserNamtarView.as_view(), name ="namtar"),
    path('put/namtar/', UserNamtarView.as_view(), name= 'put_namtar'),
    path('save/image/',UserImage.as_view(), name='save_image'),
    path('image/',UserImage.as_view(), name='view_image'),
    path('human/shape/',ShapeList.as_view(), name='shape' ),
]

if settings.DEBUG:  # Хөгжүүлэлтийн үед л ажиллана
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)