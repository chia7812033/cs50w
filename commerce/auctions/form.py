from django.forms import ModelForm
from .models import Item

class CreateListingForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'create_date', 'create_time']