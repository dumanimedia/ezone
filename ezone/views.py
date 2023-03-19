from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Brand, OrderItem, ProductReview
from django.contrib.auth.models import User
from .cart import Cart
from django.contrib import messages
from userprofile.forms import (
    ProductCreationForm,
    ProductUpdateForm,
    OrderCreationForm,
    ProductReiewCreationForm,
)
from django.db.models import Max, Min
import os


def home_view(request):
    context = {
        "products": Product.objects.all()[:8],
        "categories": Category.objects.all()[:3],
    }
    return render(request, "home.html", context)


def about_view(request):
    return render(request, "about.html", {})


def services_view(request):
    return render(request, "services.html", {})


def contact_view(request):
    return render(request, "contact.html", {})


def search_view(request):
    query = request.GET.get("q", "")
    context = {
        "query": query,
        "products": Product.objects.filter(title__icontains=query),
        "categories": Category.objects.filter(title__icontains=query)[:8],
        "brands": Brand.objects.filter(title__icontains=query),
    }
    return render(request, "search.html", context)


def products_view(request):
    context = {
        "products": Product.objects.all()[:16],
        "categories": Category.objects.all()[:5],
        "max_price": Product.objects.aggregate(Max("price"))["price__max"],
        "min_price": Product.objects.aggregate(Min("price"))["price__min"],
    }
    return render(request, "products.html", context)


def category_details_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(
        request, "category-details.html", {"category": category, "products": products}
    )


def brand_details_view(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand)

    context = {"brand": brand, "products": products}
    return render(request, "brand-details.html", context)


def product_details_view(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    relatedProducts = Product.objects.all()[:4]
    reviews = ProductReview.objects.filter(product=product)[:4]

    form = ProductReiewCreationForm()
    if request.method == "POST":
        form = ProductReiewCreationForm(request.POST)
        if not form.is_valid():
            messages.info(request, "Reviewing Product Failed")
            return redirect("my_account")

        ProductReview.objects.create(
            user=request.user,
            product=product,
            review_msg=form.cleaned_data["review_msg"],
            review_rating=form.cleaned_data["review_rating"],
        )
        messages.success(request, "The Product has been succesfully reviewed!")

    context = {
        "product": product,
        "relatedProducts": relatedProducts,
        "form": form,
        "reviews": reviews,
        "alreadyRevied": False,
    }

    return render(request, "product-details.html", context)


@login_required(login_url="login")
def create_product_view(request):
    if not User.objects.filter(pk=request.user.id, groups__name="staff").exists():
        messages.info(request, "Only authorized personel allowed!")
        return redirect("my_account")

    form = ProductCreationForm()
    if request.method == "POST":
        form = ProductCreationForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.info(request, "Product Creation Failed")
            return redirect("create_product")

        product = form.save(commit=False)
        product.user = request.user

        product.save()
        messages.success(request, "Product Created Successfully")
        return redirect("my_store")

    return render(request, "create-product.html", {"form": form})


@login_required(login_url="login")
def update_product_view(request, category_slug, slug):
    if not User.objects.filter(pk=request.user.id, groups__name="staff").exists():
        messages.info(request, "Only authorized personel allowed!")
        return redirect("my_account")

    product = get_object_or_404(Product, slug=slug)

    if not product.user == request.user:
        messages.info(request, "unauthorized User")
        return redirect("my_account")

    form = ProductUpdateForm(instance=product)
    if request.method == "POST":
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Product has been updated Successfully.")
            return redirect("my_account")

    return render(request, "update-product.html", {"product": product, "form": form})


def delete_product_view(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    if not product.user == request.user:
        messages.info(request, "unauthorized User")
        return redirect("my_account")

    if request.method == "POST":
        os.remove(product.image.path)
        messages.success(request, f'Product "{product.title}" Succesfully Deleted')
        product.delete()
        return redirect("my_account")

    return redirect("products")


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect("products")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect("cart")


def change_quantity(request, product_id):
    cart = Cart(request)
    action = request.GET.get("action", "")

    if action:
        quantity = 1

        if action == "decrease":
            quantity = -1

        cart.add(product_id, quantity, True)
    return redirect("cart")


def cart_view(request):
    return render(request, "cart.html")


@login_required(login_url="login")
def checkout_view(request):
    cart = Cart(request)
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if not form.is_valid():
            messages.info(request, "Please Use valid values!")
            return render(request, "checkout.html", {"form": form})

        total_cost = 0

        for item in cart:
            product = item["product"]
            total_cost += product.price * int(item["quantity"])

        order = form.save(commit=False)
        order.created_by = request.user
        order.email = request.user.email
        order.total_cost = total_cost
        order.save()

        for item in cart:
            product = item["product"]
            quantity = int(item["quantity"])
            price = product.price * quantity

            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=price
            )

        cart.clear()
        messages.success(request, "Order Succesfully Placed!")
        return redirect("my_account")

    return render(
        request, "checkout.html", {"form": form, "user": request.user.userprofile}
    )


def not_found_view(request):
    return render(request, "not_found.html", {})
