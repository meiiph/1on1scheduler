from django.urls import path
from . import views
from .views.invitations import InvitationListCreateView, InvitationRetrieveUpdateDestroyView
from .views.events import UserEventListView, EventAddAttendeeView, CalendarEventListView, EventCreateView, EventRemoveAttendeeView, EventCancelView, EventRequestJoinView

urlpatterns = [
    path('invitations/', InvitationListCreateView.as_view(), name='invitation-list-create'),
    path('invitations/<int:invitation_id>/', InvitationRetrieveUpdateDestroyView.as_view(), name='invitation-retrieve-update-destroy'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('my_events/', UserEventListView.as_view(), name='user_events'),
    path('add_attendee/<int:event_id>/<int:user_id>/', EventAddAttendeeView.as_view(), name='add_attendee'),
    path('remove_attendee/<int:event_id>/<int:user_id>/', EventRemoveAttendeeView.as_view(), name='remove_attendee'),
    path('cancel_event/<int:event_id>/', EventCancelView.as_view(), name='cancel_event'),
    path('calendar_events/<int:calendar_id>/', CalendarEventListView.as_view(), name='calendar_events'),
    path('request_join/<int:event_id>/<int:user_id>/', EventRequestJoinView.as_view(), name='request_join'),
]