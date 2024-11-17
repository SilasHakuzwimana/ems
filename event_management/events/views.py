from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from .models import Event
from .forms import EventForm, ReviewForm, TicketForm
from django.core.mail import send_mail # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore # noqa: F401
from django.conf import settings # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore

def dashboard(request):
    events = Event.objects.all()  # Fetch all events
    return render(request, 'events/dashboard.html', {'events': events})


def send_event_reminder(user, event):
    try:
        send_mail(
            'Event Reminder',
            f'Your event "{event.title}" is coming up!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error or handle it gracefully
        print(f"Failed to send email: {e}")


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Replace 'login' with your login URL name
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})
def login_view(request):
    next_url = request.GET.get('next', 'event_list')  # Default redirect to 'event_list'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'events/login.html', {'next': next_url})

@login_required
def profile(request):
    return render(request, 'events/profile.html')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    ticket_form = TicketForm()
    review_form = ReviewForm()  # Ensure ReviewForm is imported correctly

    if request.method == "POST":
        if "purchase_ticket" in request.POST:  # Check which form is submitted
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.event = event
                ticket.save()
                return redirect('event_detail', pk=event.pk)
        elif "submit_review" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.event = event
                review.save()
                return redirect('event_detail', pk=event.pk)

    return render(
        request, 
        'events/event_detail.html', 
        {'event': event, 'ticket_form': ticket_form, 'review_form': review_form}
    )


@login_required
def event_new(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()  # Save the event data to the database
            return redirect('event_list')  # Redirect after event creation
    else:
        form = EventForm()  # For GET requests, render an empty form

    # Render the template with the form for both GET and POST requests
    return render(request, 'events/event_new.html', {'form': form})

def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})
