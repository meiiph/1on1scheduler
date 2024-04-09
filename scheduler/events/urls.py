from django.urls import path
from .views import create, view_all_events, view_event, confirm_event, delete_event

urlpatterns = [
    path('create/<int:calendar_id>/', create, name='create-event'),
    path('list/<int:calendar_id>/',view_all_events, name='view-all'),
    path('<int:event_id>/view/', view_event, name='view-event'),
    path('<int:event_id>/respond/', confirm_event, name='confirm'),
    path('<int:event_id>/delete/', delete_event, name='delete-event'),
]