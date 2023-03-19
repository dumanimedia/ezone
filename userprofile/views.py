from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserAccountCreationForm, UserProfileCreationForm
from .decorators import unauthenticated_user
from ezone.models import Product, Order, OrderItem, Category, Brand
from .models import Userprofile


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, "Invalid Username OR Password!")
            return render(request, "login.html")

        login(request, user)
        return redirect("my_account")
    return render(request, "login.html", {})


def logout_view(request):
    logout(request)
    return redirect("login")


@unauthenticated_user
def signup_view(request):
    form = UserAccountCreationForm()
    if request.method == "POST":
        form = UserAccountCreationForm(request.POST)
        if not form.is_valid():
            messages.info(request, "Please Use valid values!")
            return render(request, "signup.html", {"form": form})

        user = form.save()
        customer_group = Group.objects.get(name="customer")
        user.groups.add(customer_group)
        Userprofile.objects.create(user=user)

        username = form.cleaned_data.get("username")

        messages.success(request, f"Account was created for {username}")
        return redirect("login")
    return render(request, "signup.html", {})


@login_required(login_url="login")
def my_account_view(request):
    context = {
        "form": UserProfileCreationForm(),
        "user": request.user.userprofile,
        "orders": Order.objects.filter(created_by=request.user),
    }

    return render(request, "userprofile.html", context)


@login_required(login_url="login")
def my_order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    if not order.created_by == request.user:
        messages.info(request, "unauthorized User")
        return redirect("my_account")

    orderItems = OrderItem.objects.filter(order=order)
    context = {"order": order, "orderItems": orderItems}

    return render(request, "order-details.html", context)


@login_required(login_url="login")
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == "POST":
        messages.success(request, f"Order '0{order_id}' Succesfully Deleted")
        order.delete()

    return redirect("my_account")


@login_required(login_url="login")
def update_my_account_view(request):
    form = UserProfileCreationForm()
    if request.method == "POST":
        form = UserProfileCreationForm(request.POST)
        if not form.is_valid():
            messages.info(request, "Account Info Update Failed")
            return render(
                request,
                "userprofile.html",
                {"form": form, "user": request.user.userprofile},
            )

        userprofile = Userprofile.objects.get(id=request.user.id)

        if userprofile:
            userprofile.first_name = form.cleaned_data["first_name"]
            userprofile.last_name = form.cleaned_data["last_name"]
            userprofile.date_of_birth = form.cleaned_data["date_of_birth"]
            userprofile.mobile = form.cleaned_data["mobile"]

            messages.success(request, "Account was updated Successfully")

            userprofile.save()
    return redirect("my_account")


@login_required(login_url="login")
def my_store_view(request):
    if not User.objects.filter(pk=request.user.id, groups__name="staff").exists():
        messages.info(request, "Only authorized personel allowed!")
        return redirect("my_account")

    context = {
        "products": Product.objects.filter(user=request.user),
        "isFirstAdmin": False,
        "users": None,
        "categories": None,
        "brands": None,
    }
    if request.user.id == 1 or "1":
        context["isFirstAdmin"] = True
        context["users"] = User.objects.all().exclude(id=request.user.id)
        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()

    return render(request, "my_store.html", context)
