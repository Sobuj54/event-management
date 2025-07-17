from django.shortcuts import render, redirect
from event.models import Event
from event.forms import EventForm
from django.contrib.auth.decorators import user_passes_test
from category.models import Category
from django.contrib import messages


# List all events
def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

@user_passes_test(is_organizer)
def organizer_dashboard(request):
    total_events = Event.objects.count()
    events = Event.objects.all()
    total_categories = Category.objects.count()

    context = {
        "total_events": total_events,
        "total_categories":total_categories,
        "events": events
    }

    return render(request,"event-list.html", context)

@user_passes_test(is_organizer)
def event_list(request):
    query = request.GET.get('q','')
    if query:
        events = Event.objects.select_related('category').prefetch_related('participants').filter(name__icontains=query)
    else:
        events = Event.objects.select_related('category').prefetch_related('participants').all()
    return render(request, 'event-list.html', {'events': events})


# Create a new event
@user_passes_test(is_organizer)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully.")
            return redirect('event:list')
    else:
        form = EventForm()
    return render(request, 'event-create.html', {'form': form})


# Update an existing event
@user_passes_test(is_organizer)
def event_update(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return redirect('event:list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:list')
    else:
        form = EventForm(instance=event)

    return render(request, 'event-update.html', {'form': form, 'event': event})


# Delete an event
@user_passes_test(is_organizer)
def event_delete(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return redirect('event:list')

    if request.method == 'POST':
        event.delete()
        return redirect('event:list')

    return render(request, 'event-delete.html', {'event': event})
