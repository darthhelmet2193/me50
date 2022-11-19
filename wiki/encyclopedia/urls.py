from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.show_entries, name="entry"),
    path("new_page", views.create_new_page, name="new_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random"),
    path("save_edit", views.save_edit, name="save_edit")
]
