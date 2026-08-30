from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models, transaction

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.BigAutoField(primary_key=True)
    avatar = models.ImageField(upload_to='img-avatar/', default='img-avatar/default-avatar.png', blank=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    email_verificado = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    rol = models.ForeignKey('Rol', on_delete=models.PROTECT, related_name='usuarios', null=True, blank=True)
    estado = models.CharField(max_length=20, default="ACTIVO")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    strikes = models.PositiveSmallIntegerField(default=0)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_cantidad_eventos(self):
        return self.eventos_creados.count()

    def aplicar_strike(self):
        """Centraliza la lógica de penalización por strikes."""
        self.strikes += 1
        if self.strikes >= 3:
            self.is_active = False
            self.estado = "BLOQUEADO"
            with transaction.atomic():
                # Desactivar foros y cancelar eventos relacionados
                self.foros.update(is_active=False)
                self.eventos_creados.exclude(estado='CANCELADO').update(estado='CANCELADO')
        self.save()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre