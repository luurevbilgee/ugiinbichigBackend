from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Login, Signup, CreateTokenView, UserView, CheckTokenView, HumanView, UserNamtarView, UserImage, ShapeList, OPT, ResetPassword, Relation

urlpatterns =[
    path('login/', Login.as_view(), name= 'login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('auth/token/',CreateTokenView.as_view(), name='token_create'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/check/', CheckTokenView.as_view(), name  ='check_token'),
    path('human/', HumanView.as_view(), name ="human"),
    path('user/namtar', UserNamtarView.as_view(), name ="user_namtar"),
    path('image/',UserImage.as_view(), name='view_image'),
    path('human/shape/',ShapeList.as_view(), name='shape' ),
    path('auth/opt/', OPT.as_view(), name='opt'),
    path('auth/resetPassword/', ResetPassword.as_view(), name='resetPassword'),
    path('relation/', Relation.as_view(), name ='relation'),
]

if settings.DEBUG:  # Хөгжүүлэлтийн үед л ажиллана
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)