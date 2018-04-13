from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'searchapp/index.html')

def product(request):
    return render(request, 'searchapp/product.html')

def myaccount(request):
    return render(request, 'searchapp/myaccount.html')

def legalnotice(request):
    return render(request, 'searchapp/legalnotice.html')
