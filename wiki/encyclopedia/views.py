from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util


def index(request):

    # List all existed entry
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

    # If not extists then go to an error page
    else:
        return HttpResponseRedirect(reverse('fault', args=[1]))


def search(request):

    title = request.GET.get("q")
    # Find if there is entry exact match
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title, "entry": entry
        })

    # Find entry's substring is match
    else:
        title = title.lower()
        results = []
        entries = util.list_entries()
        for en in entries:
            if title in en.lower():
                results.append(en)
        # Show all matched result
        return render(request, "encyclopedia/searchresult.html", {
            "results": results
        })


def new_page(request):

    # User create new page via POST
    if request.method == "POST":

        # Get the title from form
        title = request.POST.get("title")

        # If title already exists, then show an error page
        if util.get_entry(title):
            return HttpResponseRedirect(reverse('fault', args=[2]))

        # Save the page and redirect to the new page
        else:
            content = request.POST.get("content")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
    
    # Go to create a new page
    return render(request, "encyclopedia/newpage.html")


def fault(request, state):

    # Page not exists
    if state == 1:
        message = "Page does not exist"
    
    # Title duplicate
    elif state == 2:
        message = "Title already exists"

    # Render a fault page with error message
    return render(request, "encyclopedia/fault.html", {
        "message": message
    })
