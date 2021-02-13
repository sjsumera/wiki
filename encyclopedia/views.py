from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Calls template that renders page content for wiki entries
def entry(request, entry):
    page = util.get_entry(entry)
    return HttpResponse(page)