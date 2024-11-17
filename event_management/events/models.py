from django.db import models # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.utils import timezone  # type: ignore
import datetime

# User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username

# Event model with start and end times and dates

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=datetime.time(9, 0))  # Default to 9:00 AM
    end_date = models.DateField(default=timezone.now)  # Default end date same as start date
    end_time = models.TimeField(default=datetime.time(17, 0))  # Default end time to 5:00 PM
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Ticket model
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')  # Ensure each user can only purchase one ticket per event

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# Review model
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Ensure ratings are between 1 and 5
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.event.title} by {self.user.username}"

