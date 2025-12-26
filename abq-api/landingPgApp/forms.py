from django import forms

class EmailMessageForm(forms.Form):
  name = forms.CharField(max_length=100, required=True)
  phone = forms.CharField(max_length=20, required=False)
  message = forms.CharField(required=True)