from django.shortcuts import render, redirect
from event.models import Event
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from Admin.forms import AssignRoleForm
from users.forms import CreateGroupForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

def is_participant(user):
    return user.groups.filter(name="Participant").exists()

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request,"admin-dashboard.html")


@user_passes_test(is_admin, login_url="no-permission")
def view_all_groups(request):
    groups = Group.objects.all()
    return render(request, "all-groups.html", {"groups": groups})


@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    form = CreateGroupForm()

    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} created successfully.")
            return redirect("Admin:all-groups")
    return render(request, "create-group.html", {"form": form})


@user_passes_test(is_admin, login_url="no-permission")
def delete_group(request, group_id):
    if request.method == 'POST':
        group = Group.objects.get(id=group_id)
        group_name = group.name
        group.delete()
        messages.success(request, f"{group_name} Group deleted successfully")
    return redirect("Admin:all-groups")

@user_passes_test(is_admin, login_url="no-permission")
def all_users(request):
    users = User.objects.all()
    return render(request, "all-users.html", {"users": users})

@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    print(user_id)
    user = User.objects.get(id=user_id)
    print("user" , user)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            print("role: ",role)
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"{user.username} has been assigned to {role.name} role")
            return redirect("Admin:all-users")
    return render(request, "assign-role.html", {"form":form})

@user_passes_test(is_admin, login_url="no-permission")
def delete_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            messages.error(request, "You can not delete superuser")
        else:
            user_name = user.username
            user.delete()
            messages.success(request, f"{user_name} has been deleted successfully.")
    return redirect("Admin:all-users")


def all_events(request):
    events = Event.objects.all()
    total_events = Event.objects.count()
    return render(request, "all-events.html", {"events":events, "total_events":total_events})

def redirect_based_on_role(request):
    if is_admin(request.user):
        return redirect("Admin:admin-dashboard")
    elif is_organizer(request.user):
        return redirect("Admin:organizer-dashboard")
    elif is_participant(request.user):
        return redirect('Admin:participant-dashboard')
    else:
        return redirect("no-permission")
    


@login_required
def rsvp_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.user in event.participants.all():
        messages.info(request, "You have already RSVP'd to this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, f"You have successfully RSVP’d to {event.name}.")

        # Send confirmation email
        send_mail(
            subject='RSVP Confirmation',
            message=f"Hi {request.user.first_name},\n\nYou have successfully RSVP’d to {event.name} on {event.date}.",
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

    return redirect('Admin:rsvped-events')
    

@login_required
def rsvped_events(request):
    rsvped_events = request.user.events.all()  
    return render(request, "rsvp-events.html", {"events": rsvped_events})


@login_required
def remove_rsvp(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, f"You have removed your RSVP from {event.name}.")
    else:
        messages.info(request, "You have not RSVP’d to this event.")

    return redirect("Admin:rsvped-events")  # Adjust this to match your RSVP dashboard URL




