from django import forms
from django.contrib.auth import authenticate, get_user_model



User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        pass


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(max_length=17)
    region = forms.CharField()
    street = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 =forms.CharField(
        label = 'Confirm Password', 
        widget = forms.PasswordInput)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username= username)
        if qs.exists():
            raise forms.ValidationError("username already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email= email)
        if qs.exists():
            raise forms.ValidationError("email already taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("password do not match")
        return data   
