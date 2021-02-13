from django.shortcuts import render
from django.http import HttpResponse

from . import util


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
        return render(request, "encyclopedia/missingentry.html", {
        })