from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Category, Product, Substitute
from .update_tables import update_tables
from .findsubstitute import findsubstitute

import requests
import json


# Create your views here.

def index(request):
    usern = request.POST.get('username')
    passw = request.POST.get('password')
    create_user = request.POST.get('createuser')

    if create_user:
        if (usern is not None and passw is not None):
            new_user = User.objects.create_user(usern, '', passw)

    if (usern is not None and passw is not None):
        user = authenticate(username=usern, password=passw)
        if (user is not None):
            login(request, user)
            context ={'username':usern,
                      'authenticated':1}
            return render(request, 'searchapp/index.html', context)
        else:
            message ='Connexion impossible'
            context ={'message':message}
            return render(request, 'searchapp/login.html', context)

    else:
        if request.user.is_authenticated:
            usern = request.user.username
            context ={'username':usern,
                      'authenticated':1}
            return render(request, 'searchapp/index.html', context)
        else:
            return render(request, 'searchapp/index.html')


def results(request):

    query = request.GET.get('query')
    #retrieve the query from the search bar

    req = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms="+query+"&countries=en:france&search_simple=1&action=process&json=1")
    data = json.loads(req.content.decode('utf-8'))
    cat_split = data["products"][0]["categories"].split(',')
    #category = cat_split[0]
    category = cat_split
    product = [data["products"][0]["product_name"], category, data["products"][0]["nutrition_grades"]]

    # Fill the database
    #update_tables()

    #compare to the database

    #sub_list = findsubstitute(product)
    list_results = findsubstitute(product)

    if (list_results ==[]):
        message ='Pas de substitut trouvé pour ce produit.'
        sub_list = []
        prod_id = ''
        sub_id = ''
    else:
        message = 'Au moins un substitut trouvé.'
        sub_list = list_results[0]
        prod_id = list_results[1]
        sub_id = list_results[2]


    #display the result



    #tata = Category.objects.create(CategoryName="Tata")
    #tata = Category(CategoryName="Tata")
    #tata.save()

    categories = Category.objects.all()
    context = {'categories' : categories,
               'product' : product[0],
               'categ' : category,
               'grade' : product[2],
               'sublist' : sub_list,
               'prodid': prod_id,
               'subid': sub_id,
               'message' : message}

    return render(request, 'searchapp/results.html', context)


def product(request):
    prod_id = request.GET.get('prodid')
    sub_id = request.GET.get('subid')
    erase = request.GET.get('erase')

    if (erase=='1'):
        Substitute.objects.all().delete()


    #Check if the user has pressed the Save button from the results page
    if (prod_id is None or sub_id is None):
        #prod_id = 'rien du tout'
        #sub_id = 'rien du tout'
        message=''


    #Save the results -> à ajouter check the referer !!!!!!
    else:
        lprod = len(list(Substitute.objects.filter(ProdNum=prod_id)))
        if (lprod == 0):
            Substitute.objects.create(ProdNum=prod_id, SubNum=sub_id)
            #prod = Product.objects.filter(id=prod_id).first()
            #sub = Product.objects.filter(id=sub_id).first()
            message = 'Résultat sauvegardé !'
        else:
            message = 'Vous avez déjà enregistré un substitut pour ce produit.'

    substitutes = Substitute.objects.all()
    saved_list=[]

    for save in substitutes:
        product = Product.objects.filter(id=save.ProdNum).first().ProductName
        substitute =Product.objects.filter(id=save.SubNum).first().ProductName
        minilist = [product, substitute]

        saved_list.append(minilist)

    context = {'saved' : saved_list,
               'message' : message}

    return render(request, 'searchapp/product.html', context)


def myaccount(request):
    if request.user.is_authenticated:
        usern = request.user.username
        authenticated=request.user.is_authenticated
    else:
        authenticated = request.user.is_authenticated
        usern=''

    context = {'username': usern,
               'authenticated': authenticated}
    return render(request, 'searchapp/myaccount.html', context)


def dologin(request):
    return render(request, 'searchapp/login.html')

def dologout(request):
    logout(request)
    return render(request, 'searchapp/index.html')

def legalnotice(request):
    return render(request, 'searchapp/legalnotice.html')
