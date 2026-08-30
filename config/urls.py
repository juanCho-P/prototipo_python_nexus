from django.conf.urls import static
from django.contrib import admin
from django.template.backends import django
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from config import settings
from users import views

urlpatterns = [
    path('gestion-secreta-nexus/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', RedirectView.as_view(pattern_name='auth', permanent=False)),
    path('foros/', include('forums.urls')),
    path('eventos/', include('events.urls')),
    path('reportes/', include('report.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('notification/', include('notification.urls')),
    path('probar-500/', views.provocate_500, name='probar_500'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = 'forums.views.error_404_view'