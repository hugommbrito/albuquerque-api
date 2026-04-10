from django import forms

class EmailMessageForm(forms.Form):
  name = forms.CharField(max_length=100, required=True)
  phone = forms.CharField(max_length=20, required=False)
  message = forms.CharField(required=True)

class EmailServiceSolicitationForm(forms.Form):
  venture = forms.CharField(max_length=100, required=False)
  unit = forms.CharField(max_length=100, required=False)
  name = forms.CharField(max_length=100, required=False)
  document = forms.CharField(max_length=150, required=False)
  phone = forms.CharField(max_length=20, required=False)
  email = forms.EmailField(max_length=100, required=False)
  description = forms.CharField(widget=forms.Textarea, required=False)
  accepted_terms = forms.BooleanField(required=False)