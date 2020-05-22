from django import forms
from .models import MyUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class TicketForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    userAssigned = forms.ModelChoiceField(MyUser.objects.all(), required=False, label="Assigned to ticket")
    userCompleted = forms.ModelChoiceField(MyUser.objects.all(), required=False, label="Completed to ticket")
