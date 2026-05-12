from django.db import models
from django.forms import forms
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200,verbose_name='Название категории',help_text='Максимум 200 символов')

    slug = models.SlugField(max_length=200,unique=True,verbose_name='URL-адрес',help_text='URL-friendly название (латинские буквы, цифры, дефисы)')

    description = models.TextField(blank=True,null=True,verbose_name='Описание',help_text='Необязательное описание категории')

    is_active = models.BooleanField(default=True,verbose_name='Активна',help_text='Отображается ли категория на сайте')

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name

class MedicineType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название типа'
    )

    class Meta:
        verbose_name = "тип лекарства"
        verbose_name_plural = "типы лекарств"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название лекарства'
    )

    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='URL')

    description = models.TextField(
        max_length=2000,
        verbose_name='Описание лекарства'
    )

    price = models.IntegerField(
        verbose_name='Цена лекарства',
    )

    quantity = models.IntegerField(
        verbose_name='Количество лекарства'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
    )

    medicine_type = models.ForeignKey(
        MedicineType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Тип лекарства'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'medicine_type']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Component(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Имя компонента'
    )

    class Meta:
        verbose_name = "компонент"
        verbose_name_plural = "компоненты"
        ordering = ['name']

    def __str__(self):
        return self.name

class MedicineComponent(models.Model):
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name='medicine_components',
        verbose_name='Компонент'
    )

    medicine = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='medicine_components',
        verbose_name='Лекарство',
        help_text='Ссылка на лекарство'
    )

    class Meta:
        verbose_name = "компонент лекарства"
        verbose_name_plural = "компоненты лекарств"
        unique_together = ['component', 'medicine']
        indexes = [
            models.Index(fields=['component', 'medicine']),
        ]

    def __str__(self):
        return f"{self.medicine.name} - {self.component.name}"

class Orders(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает обработки'
        CONFIRMED = 'confirmed', 'Подтвержден'
        SHIPPED = 'shipped', 'Отправлен'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELLED = 'cancelled', 'Отменен'
        RETURNED = 'returned', 'Возвращен'

    class PaymentType(models.TextChoices):
        CASH = 'cash', 'Наличные при получении'
        CARD = 'card', 'Банковская карта онлайн'

    delivery_address = models.CharField(
        max_length=255,
        verbose_name='Адрес доставки'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус заказа'
    )

    order_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата заказа'
    )

    total_price = models.IntegerField(
        verbose_name='Общая цена',
        help_text='Итоговая стоимость всех товаров в заказе'
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.CARD,
        verbose_name='Тип платежа',
        help_text='Способ оплаты'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        ordering = ['-order_date']

    def __str__(self):
        return f"Заказ №{self.id} - {self.order_date}"

class OrderMedicine(models.Model):
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        related_name='order_medicines',
        verbose_name='Заказ'
    )

    medicine = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_medicines',
        verbose_name='Лекарство'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = "лекарство в заказе"
        verbose_name_plural = "лекарства в заказах"
        unique_together = ['order', 'medicine']

    def __str__(self):
        return f"{self.order.id} - {self.medicine.name} x{self.quantity}"