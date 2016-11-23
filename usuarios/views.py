from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import UpdateView
from contenido.models import Profile, Artista
from .forms import RegistroForm, UserForm, ProfileForm, ArtistaForm
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from io import BytesIO
import uuid

from django.conf import settings

# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = "register.html"
    form_class = RegistroForm
    success_url = reverse_lazy("homepage")



    def post(self, request, *args, **kwargs):
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



class ProfileModificacion(UpdateView):
    model = User
    second_model = Profile
    third_model = Artista
    template_name = 'modals/perfil-form.html'
    form_class = UserForm
    second_form_class = ProfileForm
    third_form_class = ArtistaForm
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super(ProfileModificacion, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        usuario = self.model.objects.get(id=pk)
        profile = self.second_model.objects.get(id=usuario.profile.id)

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'formProfile' not in context:
            context['formProfile'] =  self.second_form_class(instance=profile)

        try:
            artista = self.third_model.objects.get(id=usuario.artista.id)
            if 'formArtista' not in context:
                context['formArtista'] = self.third_form_class(instance=artista)
        except Artista.DoesNotExist:
            print()

        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_usuario = kwargs['pk']
        usuario = self.model.objects.get(id=id_usuario)
        profile = self.second_model.objects.get(id=usuario.profile.id)


        form = self.form_class(request.POST, instance=usuario)
        form_profile = self.second_form_class(request.POST, instance=profile)

        try:
            artista = self.third_model.objects.get(id=usuario.artista.id)
            form_artista = self.third_form_class(request.POST, instance=artista)
            existe_artista = True
            if form_artista.is_valid():
                guardar_form_artista = True
            else:
                guardar_form_artista = False
        except Artista.DoesNotExist:
            existe_artista = False
            guardar_form_artista = True
            print()

        if form.is_valid() and form_profile.is_valid() and guardar_form_artista:
            form.save()

            val_imagen = request.POST.get('upload_user_img')

            if profile.val_imagen != val_imagen and val_imagen != "":
                image_file = request.FILES['upload_user_img_file'].read()
                image_file_name = uuid.uuid4().urn[9:] + '.png'
                conn = S3Connection(settings.AWS_SECRET_KEY, settings.AWS_ACCESS_SECRET_KEY)
                bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
                k = Key(bucket)
                k.key = 'images/' + image_file_name
                k.set_contents_from_file(BytesIO(image_file), policy='public-read')
                val_imagen = 'https://s3-us-west-2.amazonaws.com/sonidoslibres/images/' + image_file_name
                profile.val_imagen = val_imagen
                profile.save()

            if existe_artista:
                artista.val_imagen = val_imagen
                form_artista.save()


            messages.success(request, '¡La información fue actualizada correctamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())




