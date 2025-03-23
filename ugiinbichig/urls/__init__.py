from django.urls import path, include

urlpatterns = [
    path('auth/', include('ugiinbichig.urls.auth_urls')),
    path('human/', include('ugiinbichig.urls.human_urls')),
    path('user/', include('ugiinbichig.urls.user_urls')),
    path('image/', include('ugiinbichig.urls.image_urls')),
    path('relation/', include('ugiinbichig.urls.relation_urls')),
    path('death/', include('ugiinbichig.urls.death_urls')),
    path('health/', include('ugiinbichig.urls.health_urls')),
    path('marriegeStatus/',include('ugiinbichig.urls.marriagStatus')),
    path('study/', include('ugiinbichig.urls.study_urls')),
    path('video/',include('ugiinbichig.urls.video_urls'))
]
