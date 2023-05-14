from django.shortcuts import render, redirect
from listings.models import ListingModelForm, Listing
from django.forms import ImageField
from django.http import HttpResponseForbidden
from orders.models import CartEntry

# Create your views here.
def new(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        l = Listing()
        l.owner_user = user
        form = ListingModelForm(request.POST, request.FILES, instance=l)

        if form.is_valid:
            form.save()
            return redirect('view', id=l.id)
            

    form = ListingModelForm()
    context['form'] = form
    return render(request, 'add.html', context)

def browse(request):
    context = {}

    listings = Listing.objects.all()

    context['listings'] = listings

    return render(request, 'listings.html', context)

def view(request, id):
    context = {}
    listing = Listing.objects.get(id=id)
    context['listing'] = listing
    return render(request, 'view.html', context)

def edit(request, id):
    context = {}
    listing = Listing.objects.get(id=id)


    if not request.user.is_authenticated:
        return redirect('login')
    if request.user != listing.owner_user:
        return HttpResponseForbidden("<h1>You can't edit that listing! It's not yours.</h1>")

    if request.method == 'POST':
        form = ListingModelForm(request.POST, request.FILES, instance=listing)

        if form.is_valid:
            form.save()
            return redirect('view', id=listing.id)

    form = ListingModelForm(instance=listing)

    form.image = ImageField(required=False, label="Image (optional)")
    context['form'] = form
    context['id'] = id

    return render(request, 'edit.html', context)
    
def delete(request, id):
    listing = Listing.objects.get(id=id)

    if not request.user.is_authenticated:
        return redirect('login')
    if request.user != listing.owner_user:
        return HttpResponseForbidden("<h1>You can't delete that listing! It's not yours.</h1>")

    if request.method == 'POST':
        listing.delete()
        return redirect('listings')
    return render(request, 'delete.html', {'listing': listing})

def add_to_cart(request, url, id):
    listing = Listing.objects.get(pk=id)
    if listing.int_inventory==0:
        return redirect(url)
    order = CartEntry(listing=listing, user_owner=request.user, quantity=1, ordered=False)
    order_qs = CartEntry.objects.filter(listing=listing, user_owner=request.user, ordered=False)

    if order_qs.exists():
        order_tmp = order_qs[0]
        order_tmp.quantity += 1
        order_tmp.save()
    else:
        order.save()

    return redirect(url)

def add_to_cart_view(request, url, id):
    listing = Listing.objects.get(pk=id)
    if listing.int_inventory == 0:
        return redirect(url)
    order = CartEntry(listing=listing, user_owner=request.user, quantity=1, ordered=False)
    order_qs = CartEntry.objects.filter(listing=listing, user_owner=request.user)

    if order_qs.exists():
        order_tmp = order_qs[0]
        order_tmp.quantity += 1
        order_tmp.save()
    else:
        order.save()

    return redirect("view",id=id)


def list_your_items(request):
    context = {}

    listings = Listing.objects.filter(owner_user=request.user)

    context['listings'] = listings

    return render(request, 'yourlistings.html', context)

def your_view(request, id):
    context = {}
    listing = Listing.objects.get(id=id)
    context['listing'] = listing
    return render(request, 'yourview.html', context)