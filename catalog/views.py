from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from catalog.models import Category, Product, MedicineType, MedicineComponent, Orders, OrderMedicine


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
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'products': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
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