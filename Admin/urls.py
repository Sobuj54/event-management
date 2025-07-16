from django.urls import path
from Admin.views import admin_dashboard, view_all_groups, delete_group, all_users, assign_role, delete_user,create_group, redirect_based_on_role, all_events, rsvp_event, rsvped_events, remove_rsvp
from event.views import organizer_dashboard

app_name="Admin"

urlpatterns = [
    path("admin-dashboard/", admin_dashboard , name="admin-dashboard"),
    path("organizer-dashboard/", organizer_dashboard, name="organizer-dashboard"),
    path("participant-dashboard/",all_events, name="participant-dashboard"),
    path("all-groups/",view_all_groups, name="all-groups"),
    path("group/delete/<int:group_id>/",delete_group, name="delete-group"),
    path("all-users/", all_users, name="all-users"),
    path("assign-role/<int:user_id>/", assign_role, name="assign-role"),
    path("delete-user/<int:user_id>/", delete_user, name="delete-user"),
    path("create-group/", create_group, name="create-group"),
    path("redirect/", redirect_based_on_role, name="redirect-url"),
    path('rsvp/<int:event_id>/', rsvp_event, name='rsvp'),
    path("rsvp/events/",rsvped_events, name="rsvped-events"),
    path("rsvp/remove/<int:event_id>/", remove_rsvp, name="remove-rsvp")
]
