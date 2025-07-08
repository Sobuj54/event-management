from django import forms
from .models import Category

class CategoryFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        for visible in self.visible_fields():
            field = visible.field
            field.widget.attrs['class'] = (
                   'w-full px-3 py-2 border border-gray-300 rounded-md '
                    'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                    'bg-gray-50 text-sm'
            )
            field.widget.attrs['placeholder'] = field.label

class CategoryForm(CategoryFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']