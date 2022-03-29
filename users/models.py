from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an Email')

        user = self.model(
            email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, date_of_birth, password, **kwargs):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            date_of_birth=date_of_birth,
            password=password,
            is_superuser=True,
            **kwargs
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField('nick', max_length=50, blank=False, null=False)
    first_name = models.CharField('Фамилия', max_length=255, blank=True, null=True)
    last_name = models.CharField('Имя', max_length=255, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    last_time_visit = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'date_of_birth', ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
