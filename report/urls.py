from django.urls import path
from . import views

urlpatterns = [
    path('foro/<int:foro_id>/', views.reportar_foro, name='reportar_foro'),
    path('comentario/<int:comentario_id>/', views.reportar_comentario, name='reportar_comentario'),
    path('evento/<int:evento_id>/', views.reportar_evento, name='reportar_evento'),
]