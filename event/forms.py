from django import forms
from event.models import Event

class EventFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            field = visible.field
            field.widget.attrs['class'] = (
                'w-full px-3 py-2 border border-gray-300 rounded-md '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50 text-sm'
            )
            field.widget.attrs['placeholder'] = field.label

class EventForm(EventFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
             'participants': forms.CheckboxSelectMultiple(),
        }