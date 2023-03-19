from .models import Category
from .cart import Cart


def categories(request):
    return {"categories": Category.objects.all()[:5]}


def ezone_address(request):
    return {
        "ezone_address": {
            "address": "7185 Cheryl Point, Lake Amanda, NJ",
            "mobile": "+(301)-602-2701",
            "mail": "sales@ezone.com",
            "facebook": "https://www.facebook.com/ezone-store",
            "twitter": "https://www.twitter.com/ezone-store",
            "pinterest": "https://www.pinterest.com/ezone-store",
            "instagram": "https://www.instagram.com/ezone-store",
            "youtube": "https://www.youtube.com/ezone-store",
        }
    }


def cart(request):
    return {"cart": Cart(request)}
