from django import forms

from .models import ContactUs

class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'title', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'rows': 5,
                'id': 'message'
            })
        }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'email': 'ایمیل'
        }
        error_messages = {
            'full_name':{
                'required': 'لطفا نام و نام خانوادگی را وارد کنید'
            }
        }