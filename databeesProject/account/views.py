from account.forms import UserCreationForm
from account.models import UserProfile as User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from databeesProject.views import index as main
from transaction.models import Sale


def login(request):
    if 'email' in request.POST and 'password' in request.POST:
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # if request.GET["next"]:
            # return HttpResponseRedirect(request.GET["next"])
            return HttpResponse("success", content_type="text/plain")
        else:
            return HttpResponse("Either Password or Email is wrong", content_type="text/plain")
    else:
        return redirect(main)

@csrf_protect
def register(request):
    args = {}
    args['form'] = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                username = request.POST.get('email', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                return HttpResponse("success", content_type="text/plain")
            except IntegrityError:
                return HttpResponse("Email is already taken", content_type="text/plain")
        else:
            # Check for errors
            return JsonResponse(form.errors)
    return redirect(main)


@login_required(login_url='/account/login/')
def profile(request):
    sale_set = Sale.objects.filter(seller=request.user)
    return render_to_response('profile.html', {'sale_set':sale_set}, RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect(main)
