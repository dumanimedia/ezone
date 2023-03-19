from django.urls import path
from . import views as v1
from userprofile import views as v2

urlpatterns = [
    path("", v1.home_view, name="home"),
    path("about/", v1.about_view, name="about"),
    path("search/", v1.search_view, name="search"),
    path("services/", v1.services_view, name="services"),
    path("contact/", v1.contact_view, name="contact"),
    path("products/", v1.products_view, name="products"),
    path("products/create", v1.create_product_view, name="create_product"),
    path("cart/", v1.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>/", v1.add_to_cart, name="add_to_cart"),
    path(
        "change-quantity/<str:product_id>/", v1.change_quantity, name="change_quantity"
    ),
    path(
        "remove-from-cart/<str:product_id>/",
        v1.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", v1.checkout_view, name="checkout"),
    path("login/", v2.login_view, name="login"),
    path("logout/", v2.logout_view, name="logout"),
    path("signup/", v2.signup_view, name="signup"),
    path("my_store/", v2.my_store_view, name="my_store"),
    path("my_account/", v2.my_account_view, name="my_account"),
    path(
        "my_account/orders/<int:order_id>", v2.my_order_details, name="my_order_details"
    ),
    path(
        "my_account/orders/delete/<int:order_id>", v2.delete_order, name="delete_order"
    ),
    path("my_account/update", v2.update_my_account_view, name="update_my_account"),
    path("not_found/", v1.not_found_view, name="not_found"),
    path(
        "brands/<slug>/",
        v1.brand_details_view,
        name="brand_details",
    ),
    path(
        "categories/<slug>/",
        v1.category_details_view,
        name="category_details",
    ),
    path(
        "<slug:category_slug>/<slug>/",
        v1.product_details_view,
        name="product_details",
    ),
    path(
        "<slug:category_slug>/<slug>/update",
        v1.update_product_view,
        name="update_product",
    ),
    path(
        "<slug:category_slug>/<slug>/delete",
        v1.delete_product_view,
        name="delete_product",
    ),
]
