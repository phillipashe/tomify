from django import forms

class ProfileForm(forms.Form):
#    name = forms.CharField(max_length = 100)
    picture = forms.ImageField()
    is_tom = forms.BooleanField(initial=False, required=False)
    
