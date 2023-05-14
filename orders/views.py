from django.shortcuts import render
from .models import OrderHistory
# Create your views here.

def index(request):
    return render(request, 'orders/index.html')

def history(request):
    context = {}
    orders = OrderHistory.objects.filter(checkout_user=request.user)
    context['orders'] = orders
    print(orders)
    return render(request, 'orders/history.html', context)