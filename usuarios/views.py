from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import RegistroForm

# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegistroForm
    success_url = reverse_lazy("homepage")



    def post(self, request, *args, **kwargs):
        uf = RegistroForm(request.POST, prefix='user')
        if request.method == 'POST':
            form = RegistroForm(request.POST)
            if form.is_valid():
                 form.save()
                 messages.success(request, 'Usuario registrado exitosamente.')
                 new_user = authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password1'],
                                         )
                 login(request, new_user)
                 return HttpResponseRedirect(reverse('homepage'))
            else:
                messages.error(request, form.errors)
                form = RegistroForm()
                token = {}
                token.update(csrf(request))
                token['form'] = form

                return render(request, 'register.html', {'form': form})



