from django.shortcuts import render, redirect
from event.models import Event
from event.forms import EventForm

# List all events
def event_list(request):
    query = request.GET.get('q','')
    if query:
        events = Event.objects.select_related('category').prefetch_related('participants').filter(name__icontains=query)
    else:
        events = Event.objects.select_related('category').prefetch_related('participants').all()
    return render(request, 'event-list.html', {'events': events})


# Create a new event
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event:list')
    else:
        form = EventForm()
    return render(request, 'event-create.html', {'form': form})


# Update an existing event
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
def event_delete(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return redirect('event:list')

    if request.method == 'POST':
        event.delete()
        return redirect('event:list')

    return render(request, 'event-delete.html', {'event': event})
