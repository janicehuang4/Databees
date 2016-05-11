from django import forms
from .models import Auction, BuyItNow, Item

class AuctionForm(forms.ModelForm):

    class Meta:
        model=Auction
        fields='__all__'
        exclude=('slug','seller',)

class BuyItNowForm(forms.ModelForm):

	class Meta:
		model=BuyItNow
		fields = '__all__'
		exclude = ('slug','seller',)
        

class ItemForm(forms.ModelForm):

    class Meta:
        model=Item
        fields='__all__'
        exclude=('category',)    
