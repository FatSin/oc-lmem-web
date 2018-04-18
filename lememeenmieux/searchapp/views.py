from django.shortcuts import render

from .models import Category, Product, Substitute
from .update_tables import update_tables


# Create your views here.

def index(request):
    return render(request, 'searchapp/index.html')


def results(request):
    #Fill the database

    #retrieve the query from the search bar

    #compare to the database


    #display the result

    update_tables()

    #tata = Category.objects.create(CategoryName="Tata")
    #tata = Category(CategoryName="Tata")
    #tata.save()

    categories = Category.objects.all()
    context = {'categories' : categories}

    return render(request, 'searchapp/results.html', context)


def product(request):
    return render(request, 'searchapp/product.html')


def myaccount(request):
    return render(request, 'searchapp/myaccount.html')


def legalnotice(request):
    return render(request, 'searchapp/legalnotice.html')
