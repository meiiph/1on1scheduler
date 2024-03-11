from django.urls import path
from . import views
from .views.invitations import InvitationListCreateView, InvitationRetrieveUpdateDestroyView

urlpatterns = [
    path('invitations/', InvitationListCreateView.as_view(), name='invitation-list-create'),
    path('invitations/<int:invitation_id>/', InvitationRetrieveUpdateDestroyView.as_view(), name='invitation-retrieve-update-destroy'),
]