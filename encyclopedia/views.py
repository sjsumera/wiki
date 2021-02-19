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
        "entrytitle": entry, "entrycontent": entrycontent})
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
    title = request.POST.get('title', None)
    content = util.get_entry(title)

    # Ensure that title and content parameters were passed and that it is
    # a valid wiki entry 
    if title and content and title.lower() in [i.lower() for i in util.list_entries()]:
        form = pages.EditEntry(initial={'content':content, 'title':title})

        return render(request, "encyclopedia/edit.html", {"title":title, "content":content, "form":form})

    else:
        return render(request, "encyclopedia/missing.html")

def saveedit(request):
    # Check if the form to edit was submitted 
    if request.method == "POST":
        # If so, collect the data from the form, save, then redirect
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
  
        util.save_entry(title, content)
        messages.success(request, "Entry Updated!")
        return HttpResponseRedirect(f"wiki/{title}")
    # If not submitting via post, just display the missing entry page 
    else: 
        return render(request, "encyclopedia/missing.html")

def search(request):
    # Get the results of the query and store all our entries in a variable
    query = request.GET.get('q')
    entries = util.list_entries()

    # Check to see if the query is an exact match for an entry
    """
        Citing this article for where I found the "Find" function
        https://stackabuse.com/python-check-if-string-contains-substring/
    """ 
    if query.lower() in [i.lower() for i in entries]:
        return HttpResponseRedirect(f"wiki/{query}")
    # If not, let's see if it's a partial match    
    else:
        fuzzy_results = []
        for entry in entries:
            if entry.lower().find(query.lower()) != -1:
                fuzzy_results.append(entry)
        if fuzzy_results:
            fuzzy_results.sort()
            return render(request, "encyclopedia/search.html", {"fuzzy_results": fuzzy_results})
        else:
            return render(request, "encyclopedia/missing.html")
                
