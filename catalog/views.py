from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Category, Product, MedicineType, MedicineComponent, Orders, OrderMedicine, Component
from users.decorators import pharmacist_required


def index(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.all().order_by('-created_at')[:8]

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'index.html', context)


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'categories/category_list.html', context={'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': page_obj,
    }

    return render(request, 'categories/category_detail.html', context)


def product_list(request):
    products = Product.objects.all()

    # Получаем параметры из GET запроса
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort')

    # Фильтрация по цене (От и До)
    if min_price:
        try:
            min_price = int(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass

    if max_price:
        try:
            max_price = int(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass

    # Сортировка товаров
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'products': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    components = MedicineComponent.objects.filter(medicine=product)

    context = {
        'product': product,
        'components': components,
    }
    return render(request, 'products/product_detail.html', context)


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/detail.html', context)


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    messages.success(request, 'Товар добавлен в корзину')
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart

    messages.info(request, 'Товар удален из корзины')
    return redirect('catalog:cart_detail')


def order_list(request):
    orders = Orders.objects.all().order_by('-order_date')
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    order_items = OrderMedicine.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/order_detail.html', context)


def contacts(request):
    return render(request, 'components/contacts.html')


# ========== ФУНКЦИИ ДЛЯ ФАРМАЦЕВТА ==========

@login_required
def pharmacist_dashboard(request):
    """Панель управления фармацевта - показывает все товары"""
    if request.user.role not in ['pharmacist', 'admin']:
        messages.error(request, 'У вас нет доступа к этой странице')
        return redirect('index')

    products = Product.objects.all().order_by('-created_at')

    context = {
        'products': products,
    }
    return render(request, 'pharmacy/dashboard.html', context)


@pharmacist_required
def add_product(request):
    """Добавление нового товара"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        medicine_type_id = request.POST.get('medicine_type')
        image = request.FILES.get('image')
        components = request.POST.getlist('components')

        if not all([name, description, price, quantity, category_id]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('catalog:add_product')

        slug = name.lower().replace(' ', '-')

        product = Product(
            name=name,
            slug=slug,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
            medicine_type_id=medicine_type_id if medicine_type_id else None,
            image=image
        )
        product.save()

        # Добавляем компоненты
        for component_id in components:
            MedicineComponent.objects.create(
                medicine=product,
                component_id=component_id
            )

        messages.success(request, f'Товар "{name}" успешно добавлен!')
        return redirect('catalog:pharmacist_dashboard')

    categories = Category.objects.filter(is_active=True)
    medicine_types = MedicineType.objects.all()
    components = Component.objects.all()

    context = {
        'categories': categories,
        'medicine_types': medicine_types,
        'components': components,
    }
    return render(request, 'pharmacy/add_product.html', context)


@pharmacist_required
def edit_product(request, pk):
    """Редактирование товара"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.category_id = request.POST.get('category')
        product.medicine_type_id = request.POST.get('medicine_type')
        product.slug = product.name.lower().replace(' ', '-')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()

        # Обновляем компоненты
        components = request.POST.getlist('components')
        MedicineComponent.objects.filter(medicine=product).delete()
        for component_id in components:
            MedicineComponent.objects.create(
                medicine=product,
                component_id=component_id
            )

        messages.success(request, f'Товар "{product.name}" обновлен!')
        return redirect('catalog:pharmacist_dashboard')

    categories = Category.objects.filter(is_active=True)
    medicine_types = MedicineType.objects.all()
    components = Component.objects.all()
    current_components = product.medicine_components.values_list('component_id', flat=True)

    context = {
        'product': product,
        'categories': categories,
        'medicine_types': medicine_types,
        'components': components,
        'current_components': current_components,
    }
    return render(request, 'pharmacy/edit_product.html', context)


@pharmacist_required
def delete_product(request, pk):
    """Удаление товара"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" удален!')
        return redirect('catalog:pharmacist_dashboard')

    return render(request, 'pharmacy/delete_product.html', {'product': product})