# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Doctor, MedicalTest

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'contact_info']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=None  # Explicitly remove help text
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=None  # Explicitly remove help text
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,  # Remove help text for username
        }

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(),
        required=False
    )
    password_confirmation = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'contact_info']  # Doctor fields only

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'] = forms.CharField(initial=user.username)
            self.fields['email'] = forms.EmailField(initial=user.email)

    def save(self, commit=True):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Set the new password

        if commit:
            user.save()
        return super().save(commit)
    
class MedicalTestForm(forms.ModelForm):
    class Meta:
        model = MedicalTest
        fields = ['name', 'description', 'price', 'availability']
