from django.urls import path
from .views import create, view_all, view_one, delete, update_owner, remove_user

urlpatterns = [
    path('create', create , name='create-calendar'),
    path('all', view_all , name='view-all-calendars'),
    path('<int:id>', view_one, name='view-one-calendar'),
    path('<int:id>/delete', delete, name='delete-calendar'),
    path('<int:id>/update/owner', update_owner, name='update-owner'),
    path('<int:id>/remove/user', remove_user, name='update-owner')
]