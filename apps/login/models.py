from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Ingrese un correo')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_ADMIN = 'admin'
    ROL_TAQUILLERO = 'taquillero'
    ROL_PASAJERO = 'pasajero'
    ROLES = [
        (ROL_ADMIN, 'Administrador'),
        (ROL_TAQUILLERO, 'Taquillero'),
        (ROL_PASAJERO, 'Pasajero'),
    ]

    email = models.EmailField(max_length=40, unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=15, choices=ROLES, default=ROL_TAQUILLERO)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f'{self.email} ({self.rol})'