from django.urls import path
from . import views

urlpatterns = [
    path("/", views.book_list, name="book-list"),
    path("<uuid:book_id>", views.book_details, name="book-details"),
]
