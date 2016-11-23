from django import forms
from django.contrib.auth.models import User
from contenido.models import Profile, Artista
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields =[
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',

        ]
        labels = {
            'username':'Nombre de usuario',
            'first_name':'Nombre',
            'last_name':'Apellido',
            'email':'Correo',
        }

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =[
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email':'Correo',
        }
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'30'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'30'}),
                   'email': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'254'}),}

        def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)

            for key in self.fields:
                self.fields[key].required = True

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['val_imagen',]
        labels = {'val_imagen':'Imágen de usuario',}
        widgets={'val_imagen':forms.HiddenInput(),}


class ArtistaForm(forms.ModelForm):
    class Meta:
        model =  Artista
        fields = ['nom_artistico', 'nom_pais', 'nom_ciudad']
        labels = {'nom_artistico':'Nombre artístico', 'nom_pais':'Pais origen', 'nom_ciudad':'Ciudad origen'}
        widgets = {'nom_artistico': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'200'}),
                   'nom_pais': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'50'}),
                   'nom_ciudad': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'50'}),}


