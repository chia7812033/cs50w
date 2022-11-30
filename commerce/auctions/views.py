from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, WatchList
from .form import CreateListingForm, BidForm, AddWatchlistForm



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

    # Create a new listing
    if request.method == "POST":
        create_listing_form = CreateListingForm(request.POST, request.FILES)
        if create_listing_form.is_valid():
            create_listing_form.save()
            messages.success(request, ('Your item was successfully added!'))
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Error saving form')

    # Select createby by the current user
    context = {}
    context['form'] = CreateListingForm(initial={"createby": request.user.id})
    return render(request, "auctions/create_listing.html", context)

def listing(request, id):

    if request.method == "POST":

        # Save bid to database
        bid_form = BidForm(request.POST, request.FILES)
        if bid_form.is_valid():
            bid_form.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))

    else:  

        # Get the current listing 
        listing = Listing.objects.get(id=id)
        context = {}
        context['listing'] = listing

        # Add a bid form
        context['bid_form'] = BidForm(initial={"listing_id": id, "user_id": request.user.id})

        # Add a add watch list form
        context['watchlist_form'] = AddWatchlistForm(initial={"listing_id": id, "user_id": request.user.id})

        # Check if the listing is in watch list
        object = WatchList.objects.filter(listing_id=id, user_id=request.user.id)

        # Disable the Add watchlist button if is in watchlist
        if object.exists():
            context['isin_watchlist'] = True
        else:
            context['isin_watchlist'] = False

        return render(request, "auctions/listing.html", context)

def add_watchlist(request, listing_id):

    # Add listing to database
    if request.method == "POST":
        addwatchlist = AddWatchlistForm(request.POST, request.FILES)
        if addwatchlist.is_valid():
            addwatchlist.save()

        # Redirect to listing page
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
    in_watchlist_id = request.user.user_watch.all().values_list('listing_id', flat=True)
    watchlist_listings = Listing.objects.filter(id__in=in_watchlist_id)
    context = {}
    context['listings'] = watchlist_listings.all()
    print(context)
    return render(request, "auctions/watchlist.html", context)
