from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False)

    class Meta:
        model = Listing
        fields = ['title', 'description',
                  'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control'}),
                                      empty_label='Select a category')
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}))
    starting_bid = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Starting Bid', 'min': '0', 'step': '0.01'}))
    image_url = forms.URLField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Image URL'}))

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Add comment', 'required': True}),
        }


class DecimalInput(forms.TextInput):
    input_type = 'number'

    def __init__(self, attrs=None, **kwargs):
        if attrs is None:
            attrs = {}
        attrs['step'] = '0.01'
        super().__init__(attrs=attrs)


class BidForm(forms.ModelForm):
    amount = forms.DecimalField(
        widget=DecimalInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bid Amount',
            'required': True,
        })
    )

    class Meta:
        model = Bid
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)
        if self.listing is not None:
            if self.listing.bids.exists():
                min_bid = self.listing.bids.last().amount + 1
            else:
                min_bid = self.listing.starting_bid + 1
            self.fields['amount'].widget.attrs['min'] = min_bid

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and self.listing is not None:
            if amount < self.listing.starting_bid:
                raise ValidationError('Bid must be at least as large as the starting bid.')
            if self.listing.bids.exists() and amount <= self.listing.bids.last().amount:
                raise ValidationError('Bid must be greater than any other bids that have been placed.')

        return amount