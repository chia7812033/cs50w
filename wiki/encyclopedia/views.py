from django.shortcuts import render
from django import forms

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search'}))

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
        return render(request, "encyclopedia/searchresult.html", {
            "results": results
        })


