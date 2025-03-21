from django.urls import path, include

urlpatterns = [
    path('auth/', include('ugiinbichig.urls.auth_urls')),
    path('human/', include('ugiinbichig.urls.human_urls')),
    path('user/', include('ugiinbichig.urls.user_urls')),
    path('image/', include('ugiinbichig.urls.image_urls')),
    path('relation/', include('ugiinbichig.urls.relation_urls')),
]
