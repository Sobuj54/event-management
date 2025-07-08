from django.shortcuts import render, redirect
from .models import Participant
from .forms import ParticipantForm

# List all participants
def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participant-list.html', {'participants': participants})


# Create a new participant
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant:list')
    else:
        form = ParticipantForm()
    return render(request, 'participant-create.html', {'form': form})


# Update an existing participant
def participant_update(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        return redirect('participant:list')

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant:list')
    else:
        form = ParticipantForm(instance=participant)

    return render(request, 'participant-update.html', {'form': form, 'participant': participant})


# Delete a participant
def participant_delete(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        return redirect('participant:list')

    if request.method == 'POST':
        participant.delete()
        return redirect('participant:list')

    return render(request, 'participant-delete.html', {'participant': participant})
