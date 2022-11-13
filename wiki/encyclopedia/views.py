from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    # Get the entry by title
    entry = util.get_entry(title)

    # If entry exists then render the page
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title, "entry": entry
        })
    else:
        return render(request, "encyclopedia/fault.html")

