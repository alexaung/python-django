from .models import Listing, Bid, Comment, Watchlist
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Max
from django.utils import timezone

from .models import Bid, Category, Listing, User, Comment
from .forms import ListingForm, BidForm, CommentForm

# This view function retrieves all active listings and renders them
# on the index page using the "auctions/index.html" template.


def index(request):
    # Retrieve all active listings from the database
    active_listings = Listing.objects.filter(is_active=True)

    # Add current price to each listing
    for listing in active_listings:
        latest_bid = listing.bids.last()
        current_price = latest_bid.amount if latest_bid else listing.starting_bid
        listing.current_price = current_price

    # Render the index page, passing the active listings to the template
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })


# This view function retrieves a single listing and renders it
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

    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            # set the created date to the current time
            listing.created_date = timezone.now()
            listing.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('listing', listing_id=listing.id)
        else:
            messages.error(request, 'Invalid form submission.')
            print(form.errors)  # for debugging
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    user = None
    if request.user.is_authenticated:
        user = request.user

    watchlist = Watchlist.objects.filter(user=user, listing=listing).exists()

    highest_bid = Bid.objects.filter(listing=listing).aggregate(Max('amount'))

    winner = None
    if not listing.is_active:
        highest_bid = Bid.objects.filter(
            listing=listing).aggregate(Max('amount'))
        if highest_bid['amount__max'] and highest_bid['amount__max'] == listing.starting_bid:
            winner = listing.creator
        else:
            highest_bidder = Bid.objects.filter(
                listing=listing, amount=highest_bid['amount__max']).first()
            if highest_bidder:
                winner = highest_bidder.bidder

    comments = Comment.objects.filter(listing=listing)

    bid_form = BidForm(request.POST or None, listing=listing)

    comment_form = CommentForm()

    context = {
        'listing': listing,
        'highest_bid': highest_bid['amount__max'],
        'watchlist': watchlist,
        'comments': comments,
        'winner': winner,
        'bid_form': bid_form,
        'comment_form': comment_form,
    }
    return render(request, 'auctions/listing.html', context)


def inactive_listings(request):
    inactive_listings = Listing.objects.filter(is_active=False)
    return render(request, "auctions/inactive_listings.html", {
        "listings": inactive_listings
    })


@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user != listing.creator:
        return redirect("listing", listing_id=listing_id)
    current_bid = Bid.objects.filter(listing=listing).aggregate(Max('amount'))
    if current_bid['amount__max']:
        winner = Bid.objects.filter(
            listing=listing, amount=current_bid['amount__max']).first().bidder
        listing.winner = winner
    listing.is_active = False
    listing.save()
    return redirect("listing", listing_id=listing_id)


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user.is_authenticated:
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.listing = listing
            if bid.amount >= listing.starting_bid and (not listing.bids.exists() or bid.amount > listing.bids.last().amount):
                bid.save()
                messages.success(request, 'Bid placed successfully.')
            else:
                messages.error(
                    request, 'Bid must be at least as large as the starting bid and greater than any other bids that have been placed.')
        else:
            messages.error(request, 'Invalid form submission.')
        return redirect("listing", listing_id=listing_id)
    else:
        return redirect('login')


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(
                content=content, listing=listing, author=request.user)
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Invalid comment form submission.')
        return redirect("listing", listing_id=listing_id)
    else:
        return redirect('login')


# @login_required
# def watchlist(request):
#     user = request.user
#     wl = Watchlist.objects.filter(user=user)

#     return render(request, "auctions/watchlist.html", {
#         "watchlist": wl
#     })

@login_required
def watchlist(request):
    user = request.user
    watchlist_entries = Watchlist.objects.filter(user=user)
    watchlist = []

    for entry in watchlist_entries:
        latest_bid = entry.listing.bids.last()
        current_price = latest_bid.amount if latest_bid else entry.listing.starting_bid
        watchlist.append((entry.listing, current_price))

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required
def watchlist_add(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            user=request.user, listing=listing).exists()
        if not watchlist:
            Watchlist.objects.create(user=request.user, listing=listing)
            messages.success(request, 'Listing added to your watchlist.')
        else:
            Watchlist.objects.filter(
                user=request.user, listing=listing).delete()
            messages.success(request, 'Listing removed from your watchlist.')
    return redirect("listing", listing_id=listing_id)


@login_required
def watchlist_remove(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            user=request.user, listing=listing).exists()
        if watchlist:
            Watchlist.objects.filter(
                user=request.user, listing=listing).delete()
            messages.success(request, 'Listing removed from your watchlist.')
    return redirect("listing", listing_id=listing_id)


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category)
    for listing in listings:
        latest_bid = listing.bids.last()
        listing.current_price = latest_bid.amount if latest_bid else listing.starting_bid
    return render(request, 'auctions/category.html', {'listings': listings, 'category': category})
