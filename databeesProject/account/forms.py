from account.models import UserProfile as User
from django import forms
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label='email', initial='email', max_length=100, required=True)
    first_name = forms.CharField(
        label='First Name', initial='First Name', max_length=100, required=True)
    last_name = forms.CharField(
        label='Last Name', initial='Last Name', max_length=100, required=True)
    password = forms.CharField(
        label="Password", initial='Password', max_length=100, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = user.email

        if commit:
            user.save()

        return user

    def clean(self):
        if self.cleaned_data.get('first_name') == "First Name" or self.cleaned_data.get('last_name') == "Last Name":
            raise ValidationError("Wrong name")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not email:
            raise ValidationError("You must enter a valid email")
            # if you don't want this functionality, just remove it.
        return email
