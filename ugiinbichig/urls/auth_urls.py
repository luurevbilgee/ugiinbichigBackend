from django.urls import path
from ugiinbichig.views import Login, Signup, CreateTokenView, UserView, OPT, ResetPassword

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('token/', CreateTokenView.as_view(), name='token_create'),
    path('user/', UserView.as_view(), name='user'),
    path('opt/', OPT.as_view(), name='opt'),
    path('resetPassword/', ResetPassword.as_view(), name='resetPassword'),
]
