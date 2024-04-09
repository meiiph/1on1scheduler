from django.urls import path
from .views import create_availability, remove_availability, view_availability

urlpatterns = [
    path('create/<int:calendar_id>', create_availability, name='create-availability'),
    path('remove/<int:calendar_id>', remove_availability, name='remove-availability'),
    path('view/<int:calendar_id>', view_availability, name='view-availability'),
]