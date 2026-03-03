from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """Клиент химчистки: ФИО, телефон, количество закрытых заказов."""
    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=20, unique=True)
    closed_orders_count = models.PositiveIntegerField('Закрытых заказов', default=0)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.full_name} ({self.phone})'


class ServiceCategory(models.Model):
    """Категория услуги."""
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'

    def __str__(self):
        return self.name


class Service(models.Model):
    """Услуга: название, базовая цена, категория."""
    name = models.CharField('Название', max_length=200)
    base_price = models.DecimalField('Базовая цена', max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Заказ: клиент, услуги, коэффициент сложности, статус, даты."""

    STATUS_ACCEPTED = 'accepted'
    STATUS_CLEANING = 'cleaning'
    STATUS_READY = 'ready'
    STATUS_ISSUED = 'issued'

    STATUS_CHOICES = [
        (STATUS_ACCEPTED, 'Принято'),
        (STATUS_CLEANING, 'В чистке'),
        (STATUS_READY, 'Готово'),
        (STATUS_ISSUED, 'Выдано'),
    ]

    COMPLEXITY_CHOICES = [
        (1.0, '1'),
        (1.3, '1.3'),
        (1.5, '1.5'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент'
    )
    services = models.ManyToManyField(
        Service,
        related_name='orders',
        verbose_name='Услуги',
        blank=True
    )
    complexity = models.DecimalField(
        'Коэффициент сложности',
        max_digits=3,
        decimal_places=1,
        choices=COMPLEXITY_CHOICES,
        default=1.0
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACCEPTED
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    ready_by_date = models.DateField('Готовность к', null=True, blank=True)
    issued_at = models.DateTimeField('Дата выдачи', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.client}'

