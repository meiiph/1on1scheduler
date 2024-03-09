from rest_framework import generics
from .models import Calendar
from .serializers import CalendarSerializer

class CalendarListCreateView(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class CalendarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer