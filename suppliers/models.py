from django.db import models
from django.db.models import ManyToManyField, ForeignKey, CharField, EmailField, DecimalField, DateTimeField
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = CharField(max_length=300, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    def __str__(self):
        return f'{self.name} ({self.model})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Supplier(models.Model):
    FACTORY = 'factory'
    RETAIL = 'retail'
    ENTREPRENEUR = 'entrepreneur'

    TYPE_CHOICES = [
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    ]

    name = CharField(max_length=300, verbose_name='Название')
    type = CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='Тип звена')
    email = EmailField(verbose_name='Email')
    country = CharField(max_length=200, verbose_name='Страна')
    city = CharField(max_length=200, verbose_name='Город')
    street = CharField(max_length=200, verbose_name='Улица')
    house_number = CharField(max_length=200, verbose_name='Номер дома')
    products = ManyToManyField(Product, verbose_name='Продукты', blank=True)
    parent = ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик',
                        null=True, blank=True, related_name='children')
    debt = DecimalField(max_digits=16, decimal_places=2, default=0, verbose_name='Задолженность',
                        help_text='Задолженность перед поставщиком в рублях')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'поставщик'
        verbose_name_plural = 'поставщики'

    @property
    def level(self):
        """
        Автоматический расчет уровня иерархии (0-2)
        """
        if self.parent is None:
            return 0

        return self.parent.level + 1

    def clean(self):
        if self.type == self.FACTORY and self.parent:
            raise ValidationError('Завод не может иметь поставщика')

        if self.type == self.FACTORY and self.debt != 0:
            raise ValidationError({
                'debt': 'Завод не может иметь задолженности. Установите 0.'
            })

        if self.parent and self.parent.pk == self.pk:
            raise ValidationError('Невозможно быть поставщиком для себя')

        if self.level > 2:
            raise ValidationError('Уровень иерархии может быть не больше 2')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
