from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("pizza", AjaxPizza.as_view()),
    path("sub",AjaxSub.as_view()),
    path("pasta",AjaxPasta.as_view()),
    path("salad",AjaxSalad.as_view()),
    path("dinner_platter",AjaxDinner_platter.as_view()),
    path("remove", views.remove, name="remove"),
    path("checkout1", views.checkout1, name="checkout1"),
    path("checkout2", views.checkout2, name="checkout2"),
    path("place", views.place, name="place"),
    path("orders", views.orders, name="orders")
]
