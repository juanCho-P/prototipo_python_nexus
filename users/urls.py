from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ----------------------------------------
    # LOGIN, REGISTRO Y DASHBOARD
    # ----------------------------------------

    path(
        'auth/', 
        views.auth_view,
        name='auth'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.registro_view,
        name='register'
    ),

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),


    # ----------------------------------------
    # PERFIL DEL USUARIO
    # ----------------------------------------

    path(
        'perfil/',
        views.perfil_view,
        name='perfil'
    ),

    path(
        'perfil/editar/',
        views.editar_perfil,
        name='editar_perfil'
    ),



    path(
        'perfil/contrasena/',
        views.cambiar_contrasena,
        name='cambiar_contrasena'
    ),


    # ----------------------------------------
    # NOTIFICACIONES
    # ----------------------------------------

    path(
        'notificaciones/marcar-leidas/',
        views.marcar_notificaciones_leidas,
        name='marcar_notificaciones_leidas'
    ),


    # ----------------------------------------
    # VERIFICACIÓN DE EMAIL
    # ----------------------------------------

    path(
        'verificar_email/<uidb64>/<token>/',
        views.verificar_email,
        name='verificar_email'
    ),

    path(
        'verificar_email/enviar/',
        views.enviar_correo_verificacion,
        name='enviar_verificacion_email'
    ),


    # ----------------------------------------
    # RECUPERACIÓN DE CONTRASEÑA
    # ----------------------------------------

    path(
        'password/recuperar/',
        auth_views.PasswordResetView.as_view(
            template_name='users/contrasena_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password/recuperar/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/contrasena_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password/restablecer/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/contrasena_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password/restablecido/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/contrasena_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


    
]