from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listings,Auction_bids, Comments, Wishlist
from django.contrib.auth.decorators import login_required


def index(request):
            
    return render(request, "auctions/index.html",{
        "listings" : Listings.objects.filter(),
    })

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
    
@login_required(login_url='/login') 
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        imageURL = request.POST["imageURL"]
        seller = request.user
        category = request.POST["category"]
        categoryModel = Category.objects.get(category_name= category)
        newListing = Listings(title=title, price=price, description=description, imageURL=imageURL, seller=seller, category=categoryModel )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))

def listing(request, listingID):
    user = request.user
    item = listingID
    if request.method == "GET":
        
        listing = Listings.objects.get(pk=int(listingID))
        get_bids = Auction_bids.objects.filter(item=int(item))
        #render comments
        get_comments = Comments.objects.filter(listing=listing).order_by("time")
        #check whether user is logged in 
        if str(user)=="AnonymousUser":
            isAnonymous = True
        else:
            isAnonymous = False
        # to prevent errors use try and except
            #check whether listing is closed or open
        isOpen = listing.isActive
        # check number of bids
        number_of_bids = len(get_bids)
        if number_of_bids == 0:
            current_bid = listing.price
        else:
            #find max bid
            current_bid = 0
            for bid in get_bids:
                current_bid = max(current_bid, int(bid.bid))
        #render category of the item
        category = listing.category
        #try and except to prevent error when user is not signed in
        try:
            # check whether user has added this item to their wishlist
            wishlist = len(Wishlist.objects.filter(user=user, item=int(item)))
            if wishlist > 0:
                get_wishlist = True
            else:
                get_wishlist = False
            #if closed, check who is the winner of the bid
            if isOpen == False:
                if current_bid != listing.price:
                    winningBid = Auction_bids.objects.get(bid=current_bid)
                    print(winningBid)
                    winner = winningBid.bidder.username
                    if str(winner) == str(user):
                        isWinner = True
                    else:
                        isWinner = False
                else:
                    isWinner = False
            else:
                isWinner = False
            #check whether user is the seller
            seller = listing.seller.username
            if str(user) == str(seller):
                isSeller = True
            else:
                isSeller = False
        # fail try: means user is not logged in
        except:
            isSeller = False
            isWinner = False
            get_wishlist = False
        # render listing website
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "get_wishlist" : get_wishlist,
            "isSeller" : isSeller,
            "number_of_bids" : number_of_bids,
            "current_bid" : current_bid,
            "comments" : get_comments,
            "anonymous" : isAnonymous,
            "isOpen" : isOpen,
            "isWinner" : isWinner,
            "category" : category,
         })
        
    if request.method == "POST":
        listing = Listings.objects.get(pk=int(listingID))
        try:
            #if user bids on item, update Auction_bids
            if request.POST["bid"]:
                user_bid = request.POST["bid"]
                if user_bid is None: 
                    return HttpResponseRedirect(reverse("listing", args=(listingID, )))
                itemBid = Listings.objects.get(pk=int(item))
                prev_bid = Auction_bids.objects.filter(item=itemBid)
                max_bid = 0
                for bid in prev_bid:
                    max_bid = max(max_bid, int(bid.bid))
                if int(user_bid) <= max_bid:
                    print("didnt bid")
                    return HttpResponseRedirect(reverse("listing", args=(listingID, )))
                newBid = Auction_bids(bidder=user,item=itemBid,bid=user_bid)
                newBid.save()
                print("bidded")
                return HttpResponseRedirect(reverse("listing", args=(listingID, )))
        
        except:
            pass
        try:
            if request.POST["submit-wishlist"]:
            # add item to wishlist table
                item_wishlist = Listings.objects.get(pk=int(item))
                newWishlist = Wishlist(user=user, item=item_wishlist)
                newWishlist.save()
                return HttpResponseRedirect(reverse("listing", args=(listingID, )))
        except:
            pass
        try:
            if request.POST["remove-wishlist"]:
            # add item to wishlist table
                item_wishlist = Listings.objects.get(pk=int(item))
                Wishlist.objects.filter(user=user, item=item_wishlist).delete()
                return HttpResponseRedirect(reverse("listing", args=(listingID, )))
        except:
           pass
        try:
            # comment section
            if request.POST["submit-comment"]:
                comment = request.POST["comment"]
                itemListing = Listings.objects.get(pk=int(item))
                #add comment, commenter, listing to Comments table
                newComment = Comments(comment=comment, listing=itemListing, commenter=user)
                newComment.save()
                print("comment saved successfully")
                return HttpResponseRedirect(reverse("listing", args=(listingID, )))
        except:
            pass
        try:    
            if request.POST["like"]:
                comment_liked = request.POST["like"]
                comment = Comments.objects.get(pk=int(comment_liked))
                comment.likes += 1
                comment.save()
                return HttpResponseRedirect(reverse("listing", args=(listingID, )))
        except:
            pass
        try:
            if request.POST["dislike"]:
                comment_disliked = request.POST["dislike"]
                comment = Comments.objects.get(pk=int(comment_disliked))
                comment.dislikes += 1
                comment.save()
                return HttpResponseRedirect(reverse("listing", args=(listingID, )))
        except:

            return HttpResponseRedirect(reverse("index"))
def openClose_listing(request, listingID):
    if request.method == "POST":
        try:
            _ = request.POST["close-listing"]
            Listings.objects.filter(pk=int(listingID)).update(isActive=False)
        except:
            Listings.objects.filter(pk=int(listingID)).update(isActive=True)
            
    return HttpResponseRedirect(reverse("listing", args=(listingID, )))

@login_required(login_url='/login') 
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, "auctions/wishlist.html",{
        "wishlist" : wishlist
    })

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html",{
        "categories": categories
    })

def category_listing(request, category):
    #get all items belonging to the category
    #incase category does not exist
    category_listing = Category.objects.get(category_name=category)
    listings = Listings.objects.filter(category=category_listing)
    print(listings)
    return render(request, "auctions/category_listing.html",{
        "listings": listings,
        "category": category
    })


