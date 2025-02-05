from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("items/<int:item_id>/", views.get_item, name="get_item"),
    path("items/", views.create_item, name="create_item"),
    path("items/<int:item_id>/update/", views.update_item, name="update_item"),
    path("items/<int:item_id>/delete/", views.delete_item, name="delete_item"),
    path("server-error/", views.server_error, name="server_error"),
    path("redirect/", views.handle_redirect, name="handle_redirect"),
]
