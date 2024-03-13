from django.urls import path
from . import views
from .views.invitations import ReceivedInvitationListCreateView, SentInvitationListCreateView, ReceivedInvitationRetrieveUpdateDestroyView, SentInvitationRetrieveUpdateDestroyView
from .views.events import UserEventListView, EventAddAttendeeView, CalendarEventListView, EventCreateView, EventRemoveAttendeeView, EventCancelView, EventRequestJoinView
from .views.calendars import Calendar_View

urlpatterns = [
    path('received_invitations/', ReceivedInvitationListCreateView.as_view(), name='received-invitation-list-create'),
    path('sent_invitations/', SentInvitationListCreateView.as_view(), name='sent-invitation-list-create'),
    path('received_invitations/<int:invitation_id>/', ReceivedInvitationRetrieveUpdateDestroyView.as_view(), name='received-invitation-retrieve-update-destroy'),
    path('sent_invitations/<int:invitation_id>/', SentInvitationRetrieveUpdateDestroyView.as_view(), name='sent-invitation-retrieve-update-destroy'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('my_events/', UserEventListView.as_view(), name='user_events'),
    path('add_attendee/<int:event_id>/<int:user_id>/', EventAddAttendeeView.as_view(), name='add_attendee'),
    path('remove_attendee/<int:event_id>/<int:user_id>/', EventRemoveAttendeeView.as_view(), name='remove_attendee'),
    path('cancel_event/<int:event_id>/', EventCancelView.as_view(), name='cancel_event'),
    path('calendar_events/<int:calendar_id>/', CalendarEventListView.as_view(), name='calendar_events'),
    path('request_join/<int:event_id>/<int:user_id>/', EventRequestJoinView.as_view(), name='request_join'),
    path('calendars/', Calendar_View.as_view(), name='calendars'),
    path('calendars/<int:calendar_id>/',Calendar_View.as_view(), name='calendar_fix')
]