import os
import requests
import json
from binascii import hexlify
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from transaction.models import Sale, Item, BuyItNow
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from math import ceil
# Create your views here.


def index(request):
    return render_to_response("index.html", RequestContext(request))


def parseRequest(getRequest):
    category = []
    queryTokens = ""
    page = 1
    low = 0
    high = 19
    fromPrice = ""
    toPrice = ""
    query = getRequest['q']
    queryTokens = query.split(' ')
    results = Item.objects.filter(keywords__name__in=queryTokens)
    if 'category' in getRequest and getRequest["category"] != "":
        category.append(getRequest['category'])
        results = results.filter(category__parent__name__in=category)
    if 'BuyItNow' in getRequest and 'Auction' in getRequest:
        pass
    elif 'BuyItNow' in getRequest:
        results = results.filter(sale__auction__isnull=True)
    elif 'Auction' in getRequest:
        results = results.filter(sale__buyitnow__isnull=True)
    if 'from' in getRequest and getRequest['from'] != "":
        fromPrice = getRequest['from']
        results = results.filter(Q(sale__buyitnow__sale_price__gte=fromPrice) | Q(
            sale__auction__current_bid__gte=fromPrice))
    if 'to' in getRequest and getRequest['to'] != "":
        toPrice = getRequest['to']
        results = results.filter(Q(sale__buyitnow__sale_price__lte=toPrice) | Q(
            sale__auction__current_bid__lte=toPrice))
    if 'page' in getRequest and getRequest['page'] != "":
        page = int(getRequest['page'])
        if page != 1:
            high = 20*page
            low = high - 20
    size = len(results)
    results = results[low:high]
    return (size, results, low, high, page, fromPrice, toPrice)


def getResultsCategories(results):
    categories = []
    for result in results:
        if hasattr(result.category, 'parent') and result.category.parent.name not in categories:
            categories.append(result.category.parent.name)
    return categories


def search(request):
    if 'q' in request.GET:
        (size, results, low, high, page, fromPrice, toPrice) = parseRequest(
            request.GET)
        categories = getResultsCategories(results)
        return render_to_response("search.html", {'results': results, 'categories': categories, 'query': request.GET['q'], 'size': size, 'pages': range(int(ceil(float(size)/20))), 'page': page, 'low': low+1, 'high': high+1, 'fromPrice': fromPrice, 'toPrice': toPrice},
                                  RequestContext(request))
    else:
        redirect(index)


def item(request):
    if 'slug' in request.GET:
        if 'cart' not in request.session:
            request.session['cart'] = []
        itemSlug = request.GET['slug']
        if itemSlug not in request.session['cart']:
            request.session['cart'].append(itemSlug)
            request.session.modified = True
        return HttpResponse("success", content_type="text/plain")
    requestSlug = request.path.split('/')[-1]
    try:
        payKey = 0
        item = Item.objects.get(Q(sale__buyitnow__slug=requestSlug) | Q(sale__auction__slug=requestSlug))
        if hasattr(item.sale, 'buyitnow'):
            unique_payment_id = hexlify(os.urandom(16))
            payKey = GeneratePayKey(item.title, item.id, item.sale.buyitnow.sale_price, unique_payment_id)
        return render_to_response("item.html", {'item': item, 'payKey':payKey}, RequestContext(request))
    except Item.DoesNotExist:
        raise 404


def test(request):
    return render_to_response("test.html", RequestContext(request))


def items(request):
    return render_to_response("items.html", RequestContext(request))


def PaypalApiCall(data, url, headers):
    req = requests.post(url, data=json.dumps(data), headers=headers)
    return req.json()

def ConvertAmountJSONCompatible(num):
    return str(round(float(num),2))

def GeneratePayKey(title, id, total, unique_id):
    paypal_dict = {
                "actionType": "PAY",
                "currencyCode": "USD",
                "item_name": title,
                "item_number": id,
                "receiverList": {
                    "receiver": [
                        {
                            "amount": ConvertAmountJSONCompatible(total),
                            "email": "daniyar.yeralin-facilitator@gmail.com"
                        }
                    ],
                },
                "returnUrl": "http://bf132fc6.ngrok.io/payments/success",
                "cancelUrl": "http://bf132fc6.ngrok.io/payments/cancel",
                "invoice": unique_id,
                "requestEnvelope": {
                    "errorLanguage": "en_US",
                    "detailLevel": "ReturnAll"
                }
            }
    headers = {
        "X-PAYPAL-SECURITY-USERID": "daniyar.yeralin-facilitator_api1.gmail.com",
        "X-PAYPAL-SECURITY-PASSWORD": "CL9CZGYHA8APN7K8",
        "X-PAYPAL-SECURITY-SIGNATURE": "Atq-fQDEqX9txppkIaBo6PtTmdcCACbUGg9tlZ6F.HCHL3i5bk9mv0oI",
        "X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T",
        "X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
        "X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON",
        "Content-Type": "application/json"
    }
    json_response = PaypalApiCall(paypal_dict, "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay", headers)
    if 'payKey' in json_response:
        return json_response['payKey']
    else:
        return -1

def cart(request):
    cart_items = []
    total = 0
    payKey = 0
    if 'cart' in request.session and len(request.session['cart']) != 0:
        cart = request.session['cart']
        for slug in cart:
            item = Sale.objects.get(slug=slug)
            total += item.buyitnow.sale_price
            cart_items.append(item)
        item = cart_items[0]
        unique_payment_id = hexlify(os.urandom(16))
        payKey = GeneratePayKey(item.item.title, item.id, total, unique_payment_id)
    return render_to_response("cart.html", {'cart_items': cart_items, 'total':total, "payKey":payKey}, RequestContext(request))

