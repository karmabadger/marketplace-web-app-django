from django.shortcuts import render
from orders.models import CartEntry, OrderHistory
from listings.models import Listing
from django.http import HttpResponseRedirect

from .forms import BillingShippingInfo, PayemntInfo

# Create your views here.
def index(request):
      context = {}
      checkoutItems = CartEntry.objects.all()
      context['checkoutItems'] = checkoutItems
      context['cart'] = CartEntry
      return render(request, 'cart/index.html', context)
      
   #return render(request, 'cart/notLoggedIn.html', {})

def delete(request, id):
      CartEntry.objects.filter(pk=id, user_owner=request.user).delete()
      context = {}
      context['checkoutItems'] = CartEntry.objects.filter(user_owner=request.user)
      return render(request, 'cart/index.html', context)

def checkout(request):
      if request.method == 'POST':
            form_shipping = BillingShippingInfo(request.POST)
            form_payment = PayemntInfo(request.POST)

            if form_shipping.is_valid() and form_payment.is_valid():
                  return HttpResponseRedirect('overview.html')
      else:
            form_shipping = BillingShippingInfo()
            form_payment = PayemntInfo()

      return render(request, 'cart/checkout.html', {'form_shipping': form_shipping, 'form_payment': form_payment})      

def overview(request):
      context= {}
      name = request.POST.get('name')
      address = request.POST.get('address')
      city = request.POST.get('city')
      state = request.POST.get('state')
      zip_code = request.POST.get('zip_code')
      items = CartEntry.objects.all()
      context['items'] = items
      context['name'] = name
      context['address'] = address
      context['city'] = city
      context['state'] = state
      context['zip_code'] = zip_code
      context['cart'] = CartEntry
      return render(request, 'cart/overview.html', context)

def confirmation(request):
      entries = CartEntry.objects.filter(user_owner=request.user, ordered=False)

      for e in entries:
            OrderHistory.objects.create(checkout_user=request.user, orders=e)
            listing = Listing.objects.filter(title_text=e.listing.title_text)
            l = listing.get(id=e.listing.id)
            print(l)
            print(l.int_inventory)
            l.int_inventory = l.int_inventory - e.quantity
            print(l.title_text)
            print(l.int_inventory)
            l.save()
            e.ordered = True
            e.save()

      return render(request, 'cart/confirmation.html', {})

def remove_quantiy(request, id):
      entries = CartEntry.objects.filter(pk=id)
      entry = entries.get(pk=id)
      listings = Listing.objects.filter(id=entry.listing.id)
      l = listings.get(id=entry.listing.id)
      e_quantity = entry.quantity
      tmp_quantity = e_quantity - 1

      if tmp_quantity > 0:
            entry.quantity = entry.quantity - 1
            entry.save()
      
      if tmp_quantity == 0:
            l.int_inventory = l.int_inventory + e_quantity
            l.save()
            CartEntry.objects.filter(pk=id).delete()
      
      context = {}
      checkoutItems = CartEntry.objects.all()
      context['checkoutItems'] = checkoutItems
      context['cart'] = CartEntry

      return render(request, 'cart/index.html', context)

def add_quantity(request, id):
      entries = CartEntry.objects.filter(pk=id)
      entry = entries.get(pk=id)
      listings = Listing.objects.filter(id=entry.listing.id)
      l = listings.get(id=entry.listing.id)
      e_quantity = entry.quantity
      tmp_quantity = e_quantity + 1
      
      if tmp_quantity <= l.int_inventory:
            entry.quantity = entry.quantity + 1
            entry.save()

      context = {}
      checkoutItems = CartEntry.objects.all()
      context['checkoutItems'] = checkoutItems
      context['cart'] = CartEntry

      return render(request, 'cart/index.html', context)