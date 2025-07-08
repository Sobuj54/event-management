from django import forms
from participant.models import Participant

class ParticipantFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            field = visible.field
            field.widget.attrs['class'] = (
                'w-full px-3 py-2 border border-gray-300 rounded-md '
                'bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
            )
            field.widget.attrs['placeholder'] = field.label


class ParticipantForm(ParticipantFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"