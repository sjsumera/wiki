"""
I learned about importing messages and the technique to display an alert on
error from here: https://stackoverflow.com/questions/47923952/python-django-
how-to-display-error-messages-on-invalid-login
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from django.contrib import messages
from . import util, wikiforms
import markdown2


def index(request):
    """
    View to pass entries into the index template to create Article navigation
    menu.
    """
    return render(request, "encyclopedia/index.html",
                  {"entries": util.list_entries()})


def entry(request, entry):
    """
    View to render page content for wiki entries. First, get content using
    get_entry function. If content, convert to markdown and render page, else,
    redirect to the missing page. Citing using "safe" in my template:
    https://docs.djangoproject.com/en/dev/ref/templates/builtins/#safe
    """
    entrycontent = util.get_entry(entry)

    if entrycontent:
        entrycontent = markdown2.markdown(entrycontent)
        return render(request, "encyclopedia/entry.html",
                      {"entrytitle": entry, "entrycontent": entrycontent})
    else:
        return HttpResponseRedirect("../missing")


def new(request):
    """
    View to render page when user wants to create a new entry.
    Create a new form instance by calling on FormEntry method in wikiforms.py
    then pass that variable into the template.
    """
    form = wikiforms.FormEntry()

    return render(request, "encyclopedia/new.html", {"form": form})


def newsubmit(request):
    """
    View to process new article submission request. Use casefold method to see
    if article exists already. If it doesn't exist, create it, else display
    error. I had originally used the "lower" method but learned
    casefold is a stronger way of comparing strings with Python3:
    https://www.geeksforgeeks.org/case-insensitive-string-comparison-in-python/
    I also used a list comprehension to reduce lines of code.
    I learned about that here: https://www.w3schools.com/python/python_lists_
    comprehension.asp
    """
    title = request.POST.get('title', None)
    content = request.POST.get('content', None)

    if title.casefold() not in [i.casefold() for i in
                                util.list_entries()]:
        util.save_entry(title, content)
        messages.success(request, "Entry Created!")
        return HttpResponseRedirect(f"wiki/{title}")
    else:
        messages.error(request, 'Entry Already Exists!')
        return HttpResponseRedirect("new")


def edit(request):
    """
    View to allow users to edit articles. Get content from the page that the
    user was on then prefill an edit form with that data. Also check to ensure
    the user is trying to edit a valid page. If not, show missing page.
    """
    title = request.POST.get('title', None)
    content = util.get_entry(title)

    if title and content and title.casefold() in [i.casefold() for i in
                                                  util.list_entries()]:
        form = wikiforms.FormEntry(initial={'content': content,
                                            'title': title})
        return render(request, "encyclopedia/edit.html",
                      {"title": title, "content": content, "form": form})
    else:
        return HttpResponseRedirect("missing")


def saveedit(request):
    """
    View to process saving edits. Get content from the form submission then
    run the save_entry function to update the content. Present a success
    message on redirect.
    """

    title = request.POST.get('title', None)
    content = request.POST.get('content', None)

    util.save_entry(title, content)
    messages.success(request, "Entry Updated!")
    return HttpResponseRedirect(f"wiki/{title}")


def search(request):
    """
    View to handle searching for articles. Get's the results of the user's
    query to see if the query is an exact or partial match for an entry.
    Citing this article for where I found the "Find" function
    https://stackabuse.com/python-check-if-string-contains-substring/
    """
    query = request.GET.get('q')
    entries = util.list_entries()

    # Check if query is an exact match for an entry
    if query.casefold() in [i.casefold() for i in entries]:
        return HttpResponseRedirect(f"wiki/{query}")
    # If not an exact match, check to see if it's a partial match
    else:
        fuzzy_results = []
        for entry in entries:
            if entry.lower().find(query.lower()) != -1:
                fuzzy_results.append(entry)
        # If the fuzzy match has data, render a page that shows the matches
        if fuzzy_results:
            fuzzy_results.sort()
            return render(request, "encyclopedia/search.html",
                          {"fuzzy_results": fuzzy_results})
        # If not, display empty page
        else:
            return HttpResponseRedirect("missing")


def random(request):
    """
    Gets all entries currently in the list and selects a random number
    between 0 and the length of the list. The random number is used as an
    index number when redirecting the user.
    """
    entries = util.list_entries()
    index = randint(0, len(entries))

    return HttpResponseRedirect(f"wiki/{entries[index]}")


def missing(request):
    """
    If page isn't valid, redirect the user to the missing content page
    """
    return render(request, "encyclopedia/missing.html")


def error_404(request, exception):
    """
    Custom 404 page for the site. The missing template is general enough
    for this so just using the same missing.html template.
    Citing: https://www.geeksforgeeks.org/built-in-error-views-in-django/
    """
    return render(request, "encyclopedia/missing.html")
