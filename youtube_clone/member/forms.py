from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm

from django.contrib.auth.models import User

from base.models import CreatorProfile


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    # last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    # is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-check"}))
    # is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-check"}))
    # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-check"}))
    # date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')



class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = ('profile_picture', 'bio')

        widgets = {
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description", 'maxlength': '350'}),
        }



class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}))
    new_password1 = forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}))
    new_password2 = forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
