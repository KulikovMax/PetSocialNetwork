from django import forms

from .models import Profile, User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Media:
        extend = False
        css = {
            'all': ('static/styles.css',)
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_conf = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def confirm_password(self):
        clean_data = self.cleaned_data
        if clean_data['password'] != clean_data['password_conf']:
            raise forms.ValidationError('Passwords do not match')
        return clean_data['password_conf']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)
