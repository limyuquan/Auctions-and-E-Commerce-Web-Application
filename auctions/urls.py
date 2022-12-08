from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<str:listingID>", views.listing, name="listing"),
    path("listing/<str:listingID>/close-open-listing", views.openClose_listing, name="close-open"),
    path("wishlist", views.wishlist, name="wishlist" ),
    path("category", views.category, name="category" ),
    path("category/<str:category>", views.category_listing, name="category_listing"),
]
