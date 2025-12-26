from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class CustomUser(AbstractUser):
    departament = CharField(max_length=300, verbose_name='Отдел')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
