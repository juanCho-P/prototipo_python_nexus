from django.urls import path
from . import views

urlpatterns = [
    # Buscar / listar foros
    path(
        '', 
        views.buscar_foro,
        name='buscar_foro'),


    path(
        'foro/<int:foro_id>/editar/', 
        views.editar_foro, 
        name='editar_foro'
    ),

    # Mis foros
    path(
        'mis-foros/',
        views.mis_foros_view,
        name='mis_foros'
    ),

    path(
        'mis-guardados/', 
        views.mis_foros_guardados, 
        name='mis_foros_guardados'),

    # Crear foro
    path(
        'crear/',
        views.crear_foro,
        name='crear_foro'
    ),

    # Detalle
    path(
        '<int:foro_id>/',
        views.detalle_foro,
        name='foro_detalle'
    ),

    path(
        'guardar/<int:foro_id>/',
          views.guardar_foro_toggle,
            name='guardar_foro_toggle'
    ),
    path(
        'guardados/',
          views.mis_foros_guardados,
            name='mis_foros_guardados'
        ),

    # Eliminar foro
    path(
        '<int:foro_id>/eliminar/',
        views.eliminar_foro,
        name='eliminar_foro'
    ),

    # Eliminar comentario
    path(
        'comentario/<int:pub_id>/eliminar/',
        views.eliminar_publicacion,
        name='eliminar_comentario'
    ),

    # Reportar
    path(
        'reportar/',
        views.reportar_contenido,
        name='reportar_contenido'
    ),


]