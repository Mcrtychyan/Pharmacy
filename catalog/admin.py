# catalog/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, MedicineType, Product, Component,
    MedicineComponent, Orders, OrderMedicine,
    User, UserReviews
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


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
    list_display = ('id', 'name', 'category', 'medicine_type', 'price', 'quantity', 'created_at')
    list_display_links = ('name',)
    list_editable = ('price', 'quantity')
    list_filter = ('category', 'medicine_type', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    inlines = [MedicineComponentInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'medicine_type', 'description')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'quantity')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'phone')
    list_filter = ('date_dirth',)
    search_fields = ('name', 'surname', 'email', 'phone')
    ordering = ('surname', 'name')
    readonly_fields = ('email',)

    def last_name(self, obj):
        return obj.surname

    last_name.short_description = 'Фамилия'

    def first_name(self, obj):
        return obj.name

    first_name.short_description = 'Имя'


@admin.register(UserReviews)
class UserReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medicine', 'rating', 'reviews_date')
    list_filter = ('rating', 'reviews_date', 'medicine')
    search_fields = ('user__name', 'user__surname', 'medicine__name', 'comment')
    ordering = ('-reviews_date',)
    readonly_fields = ('reviews_date',)

    fieldsets = (
        ('Информация об отзыве', {
            'fields': ('user', 'medicine', 'rating', 'comment')
        }),
        ('Дата', {
            'fields': ('reviews_date',),
            'classes': ('collapse',)
        }),
    )