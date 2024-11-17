from django import forms # type: ignore
from .models import Event, Review, Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'location',
            'capacity',
        ]

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event']  # Only need to show event for ticket purchase

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {  # Add labels for rating and comment fields
            'rating': 'Rating',
            'comment': 'Comment',
        }