from django.urls import path
from .views import ContactListCreateView, ContactRetrieveUpdateDestroyView

urlpatterns = [
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactRetrieveUpdateDestroyView.as_view(), name='contact-retrieve-update-destroy'),
]
