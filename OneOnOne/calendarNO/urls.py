from django.urls import path
from .views import CalendarListCreateView, UserEventListView, EventAddAttendeeView, CalendarRetrieveUpdateDestroyView 
from . import views

urlpatterns = [
    path('calendars/', CalendarListCreateView.as_view(), name='calendar-list-create'),
    path('calendars/<int:pk>/', CalendarRetrieveUpdateDestroyView.as_view(), name='calendar-retrieve-update-destroy'),
    path('create_event/', views.EventCreateView.as_view(), name='create_event'),
    path('my_events/', UserEventListView.as_view(), name='user_events'),
    path('delete_event/<int:pk>/', views.EventDeleteView.as_view(), name='delete_event'),
    path('add_attendee/<int:pk>/', EventAddAttendeeView.as_view(), name='add_attendee'),
    path('remove_attendee/<int:pk>/', views.EventRemoveAttendeeView.as_view(), name='remove_attendee'),
    path('cancel_event/<int:pk>/', views.EventCancelView.as_view(), name='cancel_event'),
    path('request_join/<int:pk>/', views.EventRequestJoinView.as_view(), name='request_join'),
]