from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
"""
I learned about importing messages and the technique to
   display an alert on error from here:
   https://stackoverflow.com/questions/47923952/python-django-how-to-display-error-messages-on-invalid-login 
""" 
from django.contrib import messages

from . import util
from . import pages

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Calls template that renders page content for wiki entries
def entry(request, entry):

    # Get entry content using the get_entry function 
    entrycontent = util.get_entry(entry)

    """
     Determine if there is any content to render, if so, do it
     Else, display template saying content doesn't exist 
    """
    
    if entrycontent:
        return render(request, "encyclopedia/entry.html", {
        "entrytitle": entry, "entrycontent": entrycontent })
    else: 
        return render(request, "encyclopedia/missing.html", {
        })    

def new(request):
    # Process for data if user is submitting form 
    if request.method == "POST":
        form = pages.NewEntry(request.POST)
        title = form['title'].value()

        """
        Check to see if data is valid and that an entry doesn't already exist
        Switch to lowercase to make case-insensitive and ensure data isn't overwritten. I used a list comprehension to update to lowercase, I learned about that here: https://www.w3schools.com/python/python_lists_comprehension.asp
        """
        if form.is_valid() and title.lower() not in [i.lower() for i in util.list_entries()]:
            # If entry doesn't exist create it and redirect to the new article and
            # show success message 
            util.save_entry(title, form['content'].value())
            messages.success(request, "Entry Created!")
            return HttpResponseRedirect(f"wiki/{title}")
        else:     
            messages.error(request, 'Entry Already Exists!')
    else:
        form = pages.NewEntry()

    return render(request, "encyclopedia/new.html", {"form":form} )

def edit(request):
    # Get the results passed in from the page where the user clicked "edit"
    title = request.GET.get('title', None)
    content = request.GET.get('content', None)

    # Ensure that title and content parameters were passed and that it is
    # a valid wiki entry 
    if title and content and title in [i for i in util.list_entries()]:
        return render(request, "encyclopedia/edit.html", {"title":title, "content":content})
    else:
        return render(request, "encyclopedia/missing.html")