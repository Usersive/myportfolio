from django import forms
from .models import Subscriber, Profile


class EmailForm(forms.Form):
    sender_name = forms.CharField(max_length=100)
    sender_email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    subject=forms.CharField(max_length=250, required=True)
    


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'experience', 'phone', 'email_add', 'address', 'freelance']
