from django.shortcuts import render
from django.utils import timezone
from event.models import Event

# Create your views here.
def home(request):
    today = timezone.now()
    upcoming_events = Event.objects.filter(date__gt=today).order_by("date")
    return render(request, "home.html", {"upcoming_events": upcoming_events})