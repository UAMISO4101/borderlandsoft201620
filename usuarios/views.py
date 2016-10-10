from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from .forms import RegistroForm

# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegistroForm
    success_url = reverse_lazy("homepage")

    #def post(self, request, *args, **kwargs): uf = RegistroForm(request.POST, prefix='user')
    #   upf = UserProfileForm(request.POST, prefix='artistaprofile')
    #    if uf.is_valid() and upf.is_valid():
    #        user = uf.save()
    #        userprofile = upf.save(commit=False)
    #        userprofile.user = user
    #        userprofile.save()

    #    return django.http.HttpResponseRedirect('/')

