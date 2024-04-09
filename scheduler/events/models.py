from django.db import models
from django.contrib.auth.models import User
from calendars.models import Calendar
from django.db import models
from django.contrib.auth.models import User
from calendars.models import Calendar

class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events')
    invited_user = models.ManyToManyField(User, related_name='invited_events')
    valid_from = models.DateField()
    valid_to = models.DateField()
    start = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    confirmation_status = models.BooleanField(default=False)

def schedule(self):
        """
        randomly schedule an event for the given duration. 
        """
        availabilities = self.find_intersection()
        if not availabilities:
            self.start_time = None
            self.end_time = None

        if availabilities:
            random_availability = random.choice(availabilities)
            self.start_time = random_availability[0]
            self.end_time = random_availability[0] + self.duration
        

    def find_intersection(self):
        """
        finds the common overlapping availabilities for the event. 
        """
        host_availabilities = Availability.objects.filter(events=self, user=self.host)
        guest_availabilities = Availability.objects.filter(events=self, user=self.invited_user)

        start_times = []
        end_times = []

        for availability in host_availabilities:
            host_start = availability.start_time
            host_end = availability.end_time

            for guest_availability in guest_availabilities:
                guest_start = guest_availability.start_time
                guest_end = guest_availability.end_time

                start = max(host_start, guest_start)
                end = min(host_end, guest_end)
                if start < end  and end - start >= self.duration:
                    start_times.append(start)
                    end_times.append(end)


        start_times = sorted(start_times)
        end_times = sorted(end_times)

        total_availability = []

        i = 0
        while i < len(end_times):
            start = start_times[i]
            end = end_times[i]
            total_availability.append([start, end])
            i += 1

        return total_availability




class Availability(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
