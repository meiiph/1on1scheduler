from django.urls import path
from . import views
from .views.invitations import InvitationListCreateView, InvitationRetrieveUpdateDestroyView
from .views.events import UserEventListView, EventAddAttendeeView, EventCreateView, EventDeleteView, EventRemoveAttendeeView, EventCancelView, EventRequestJoinView

urlpatterns = [
    path('invitations/', InvitationListCreateView.as_view(), name='invitation-list-create'),
    path('invitations/<int:invitation_id>/', InvitationRetrieveUpdateDestroyView.as_view(), name='invitation-retrieve-update-destroy'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('my_events/', UserEventListView.as_view(), name='user_events'),
    path('delete_event/<int:pk>/', EventDeleteView.as_view(), name='delete_event'),
    path('add_attendee/<int:pk>/', EventAddAttendeeView.as_view(), name='add_attendee'),
    path('remove_attendee/<int:pk>/', EventRemoveAttendeeView.as_view(), name='remove_attendee'),
    path('cancel_event/<int:pk>/', EventCancelView.as_view(), name='cancel_event'),
    path('request_join/<int:pk>/', EventRequestJoinView.as_view(), name='request_join'),
]