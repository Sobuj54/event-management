from django import forms
from django.contrib.auth.models import Group
from event.forms import EventFormMixin

class AssignRoleForm(EventFormMixin ,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )
