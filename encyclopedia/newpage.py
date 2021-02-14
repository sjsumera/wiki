# Read documentation found here:
# https://docs.djangoproject.com/en/3.0/topics/forms/

from django import forms

# Create form to make a new wiki entry
class NewEntry(forms.Form):
    
    title = forms.CharField(label='Article Name', max_length=50, required=True)

    content = forms.CharField(label="Write your article", required=True)

class EditEntry(NewEntry):

    title = forms.CharField(label='Article Name', max_length=50, required=True)

    content = forms.CharField(label="Write your article", required=True)