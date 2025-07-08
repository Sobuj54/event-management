from django.shortcuts import render
from event.models import Event
from participant.models import Participant
from django.utils import timezone

# Create your views here.
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.filter(participants__isnull=False).distinct().count()

    today = timezone.localdate()
    upcoming_events_count = Event.objects.filter(date__gt=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()

    query = request.GET.get("q","all")
    print(query)
    if query == "today":
        events = Event.objects.select_related("category").prefetch_related("participants").filter(date=today)
    elif query == "past":
        events = Event.objects.select_related("category").prefetch_related("participants").filter(date__lt=today)
    elif query == "all":
        events = Event.objects.select_related("category").prefetch_related("participants").all()
    elif query == "upcoming":
        events = Event.objects.select_related("category").prefetch_related("participants").filter(date__gt=today)
    

    context = {
        "total_events": total_events,
        "total_participants": total_participants,
        "past_events_count":past_events_count,
        "upcoming_events_count": upcoming_events_count,
        "events": events,
        "type": query.capitalize()
    }

    return render(request,"todays-events.html", context)


