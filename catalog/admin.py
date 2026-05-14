# catalog/admin.py
from django.contrib import admin
from django.utils.html import format_html
from image_uploader_widget.widgets import ImageUploaderWidget
from django.db import models
from .models import (
    Category, MedicineType, Product, Component,
    MedicineComponent, Orders, OrderMedicine,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'icon_preview', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Используем ImageUploaderWidget 1для поля icon_image
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 8px; object-fit: cover;" />',
                obj.icon_image.url
            )
        return '-'

    icon_preview.short_description = 'Иконка (превью)'


@admin.register(MedicineType)
class MedicineTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


class MedicineComponentInline(admin.TabularInline):
    model = MedicineComponent
    extra = 1
    fields = ('component',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'medicine_type', 'price', 'quantity', 'image_preview', 'created_at')
    list_display_links = ('name',)
    list_editable = ('price', 'quantity')
    list_filter = ('category', 'medicine_type', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    inlines = [MedicineComponentInline]

    # Используем ImageUploaderWidget для поля image
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'medicine_type', 'description')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'quantity')
        }),
        ('Изображение', {
            'fields': ('image',),
            'description': 'Загрузите изображение товара (рекомендуемый размер: 300x300 пикселей)'
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Превью'


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(MedicineComponent)
class MedicineComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'component')
    list_filter = ('medicine', 'component')
    search_fields = ('medicine__name', 'component__name')


class OrderMedicineInline(admin.TabularInline):
    model = OrderMedicine
    extra = 1
    fields = ('medicine', 'quantity')


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'payment_type', 'status', 'order_date')
    list_display_links = ('id',)
    list_editable = ('status',)
    list_filter = ('status', 'payment_type', 'order_date')
    search_fields = ('user__username', 'delivery_address', 'id')
    ordering = ('-order_date',)
    readonly_fields = ('order_date',)
    inlines = [OrderMedicineInline]

    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'delivery_address', 'status', 'payment_type')
        }),
        ('Финансы', {
            'fields': ('total_price',)
        }),
        ('Даты', {
            'fields': ('order_date',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderMedicine)
class OrderMedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'medicine', 'quantity')
    list_filter = ('order', 'medicine')
    search_fields = ('order__id', 'medicine__name')