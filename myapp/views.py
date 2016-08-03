# coding=utf-8
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.generic import CreateView
from jsonify.convert import jsonify
import simplejson
from myapp.form import UserCreationForm

from myapp.models import Message


@login_required
def index(request):
    mes = Message.objects.all()
    context = {
        'messages': mes,
    }
    return render(request, 'myapp/home.html', context)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    args = {}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            args['login_error'] = u"Пользователь не найден"
            return render(request, 'myapp/login.html', args)
    else:
        return render(request, 'myapp/login.html', args)


def registr(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            user = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                     password=newuser_form.cleaned_data['password2'])
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Заполните все поля"
            args['form'] = newuser_form
            return render(request, 'myapp/register.html', args)
    return render(request, 'myapp/register.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'myapp/register.html'

    success_url = reverse_lazy('login')


def send_message(request):
    if request.method == "POST":
        q = request.POST.get('message', '')
        if q is not None:
            new = Message.objects.create(message=q, sender=request.user)
            new.save()
    return HttpResponse('')


def receive(request):
    args = []
    if request.method == "POST":
        post = request.POST.get('offset', '')
        mes = Message.objects.filter(pk__gt=post).order_by('pk')
        for i in mes:
            args.append({'id': i.id,
                         'message': i.message,
                         'sender': i.sender.username
                         })

            arr = dict([('result', args)])
            #print(arr['result'])
            return HttpResponse(json.dumps(arr), content_type="application/json")


def sync(request):
    args = {}
    m = Message.objects.order_by('-pk')
    if m:
        args['lmid'] = m[0].id
    else:
        args['lmid'] = 0
    return HttpResponse(json.dumps(args))
