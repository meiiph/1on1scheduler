from django.urls import path
from .views import send_invitation, view_all, respond, delete_invitation, view_one

urlpatterns = [
    path('<int:calendar_id>/send', send_invitation, name='send-invitation'),
    path('all', view_all, name='view-all-invites'),
    path('<int:id>', view_one, name='view-one-invite'),
    path('<int:invitation_id>/respond', respond, name='inviation-response'),
    path('<int:invitation_id>/delete', delete_invitation, name='delete-invitation')
]