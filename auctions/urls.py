from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path('<int:listing_id>/add_to_watchlist/', views.watchlist_add, name='add_to_watchlist'),
    path('<int:listing_id>/remove_from_watchlist/', views.watchlist_remove, name='remove_from_watchlist'),
    path('<int:listing_id>/place_bid/', views.place_bid, name='place_bid'),
    path('<int:listing_id>/close_listing/', views.close_listing, name='close_listing'),
    path('<int:listing_id>/add_comment/', views.add_comment, name='add_comment'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("inactive_listings", views.inactive_listings, name="inactive_listings")
]


