from django import forms

class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'نام کاربری',
            'class':'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder':'رمز عبور',
            'class':'form-control'
        })
    )