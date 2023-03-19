from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from ezone.models import Product, Order, ProductReview
from .models import Userprofile


class UserAccountCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserProfileCreationForm(ModelForm):
    class Meta:
        model = Userprofile
        fields = ("first_name", "last_name", "mobile", "date_of_birth")


class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        exclude = ["slug", "user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formClass = {
            "class": "form-control",
        }
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(formClass)

        self.fields["image"].widget.attrs.update({"accept": "image/*"})
        self.fields["description"].widget.attrs.update({"rows": "5"})


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        exclude = ["user", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formClass = {
            "class": "form-control",
        }
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(formClass)
        self.fields["description"].widget.attrs.update({"rows": "5"})


class OrderCreationForm(ModelForm):
    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "mobile",
            "zipcode",
            "address",
            "city",
        )


class ProductReiewCreationForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ("review_msg", "review_rating")
