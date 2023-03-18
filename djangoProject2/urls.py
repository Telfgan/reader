from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from DjangoReader import views

urlpatterns = [
    path('', views.about, name = 'home'),
    path('upload/', views.image_upload_view, name = 'upload'),
    path('auth/', views.user_login, name = 'auth'),
    path('register/', views.register, name = 'register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
