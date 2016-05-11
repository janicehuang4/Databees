from django.shortcuts import render
from django.forms.formsets import formset_factory
from .forms import AuctionForm, BuyItNowForm, ItemForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Item
# Create your views here.


@csrf_protect
@login_required(login_url='/account/login/')
def create_listing(request):
    args = {}
    if request.method == 'POST':
        if 'sell_type' in request.POST and request.POST["sell_type"]=="buyItNow":
            itemForm = ItemForm(request.POST, request.FILES)
            buyItNowForm = BuyItNowForm(request.POST)
            if itemForm.is_valid() and buyItNowForm.is_valid():
                itemObject = itemForm.save()
                buyItNowObject = buyItNowForm.save(commit=False)
                buyItNowObject.item = itemObject
                buyItNowObject.seller = request.user
                buyItNowObject.save()
                return redirect('/item/'+buyItNowObject.slug)
            else:
                return render_to_response("sell.html", RequestContext(request))
        else:
            itemForm = ItemForm(request.POST, request.FILES)
            auctionForm = AuctionForm(request.POST)
            if itemForm.is_valid() and auctionForm.is_valid():
                itemObject = itemForm.save()
                auctionObject = auctionForm.save(commit=False)
                auctionObject.item = itemObject
                auctionObject.seller = request.user
                auctionObject.save()
                return redirect('/item/'+auctionObject.slug)
            else:
                return render_to_response("sell.html", RequestContext(request))
    else:
        return render_to_response("sell.html", RequestContext(request))
