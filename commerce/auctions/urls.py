from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addwatchlist/<int:listing_id>", views.add_watchlist, name="addwatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]


