# Read documentation found here:
# https://docs.djangoproject.com/en/3.0/topics/forms/

from django import forms

# Create form to edit existing entry 
class EditEntry(forms.Form):

    title = forms.CharField(label='Article Title', max_length=50, required=True)

    # Only provide textarea when editing 
    content = forms.CharField(widget=forms.Textarea, label="Edit this article", required=True)

# Create form to make a new wiki entry
class NewEntry(EditEntry):
    
    title = forms.CharField(label='Article Title', max_length=50, required=True)

    content = forms.CharField(label="Write your article")

    