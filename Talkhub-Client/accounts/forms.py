from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    userid = forms.CharField(max_length=10, label='UserID')

    class Meta:
        model = User
        fields = ['name', 'email', 'userid', 'password']

    def clean_userid(self):
        userid = self.cleaned_data.get('userid')
        if not userid.isdigit() or len(userid) != 10:
            raise forms.ValidationError("UserID must be exactly 10 digits.")
        if User.objects.filter(userid=userid).exists():
            raise forms.ValidationError("This UserID already exists.")
        return userid

class LoginForm(forms.Form):
    userid = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
