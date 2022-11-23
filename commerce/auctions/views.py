from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Listing
from .form import CreateListingForm, BidForm



def index(request):
    
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):

    if request.method == "POST":
        create_listing_form = CreateListingForm(request.POST, request.FILES)
        if create_listing_form.is_valid():
            create_listing_form.save()
            messages.success(request, ('Your item was successfully added!'))
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Error saving form')

    context = {}
    context['form'] = CreateListingForm(initial={"createby": request.user.id})
    return render(request, "auctions/create_listing.html", context)

def listing(request, id):
    if request.method == "POST":
        bid_form = BidForm(request.POST, request.FILES)
        if bid_form.is_valid():
            bid_form.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))

    else:
        listing = Listing.objects.get(id=id)
        context = {}
        context['listing'] = listing
        context['bid_form'] = BidForm(initial={"listing_id": id, "user_id": request.user.id})

        return render(request, "auctions/listing.html", context)
