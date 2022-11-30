from django import forms
from .models import Listing, Bid, WatchList

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['id', 'create_date', 'create_time']
        widgets = {'createby': forms.HiddenInput()}

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        widgets = {'listing_id': forms.HiddenInput(), 'user_id': forms.HiddenInput()}
        exclude = []

class AddWatchlistForm(forms.ModelForm):
    class Meta:
        model = WatchList
        exclude = []
        widgets = {'listing_id': forms.HiddenInput(), 'user_id': forms.HiddenInput()}
