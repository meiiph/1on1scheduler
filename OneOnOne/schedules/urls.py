from django.urls import path
from .views import ScheduleListCreateView, ScheduleRetrieveUpdateDestroyView

urlpatterns = [
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleRetrieveUpdateDestroyView.as_view(), name='schedule-retrieve-update-destroy'),
]
