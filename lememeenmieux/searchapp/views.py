from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Category, Product, Substitute, Update
from .update_tables import update_tables
from .findsubstitute import findsubstitute

import requests
import json
import datetime


# Create your views here.

def index(request):
    usern = request.POST.get('username')
    passw = request.POST.get('password')
    create_user = request.POST.get('createuser')
    prod_id = request.POST.get('prodid')
    sub_id = request.POST.get('subid')



    if create_user:
        if (usern is not None and passw is not None):
            new_user = User.objects.create_user(usern, '', passw)
            message_bis = new_user.username

    if (usern is not None and passw is not None):
        user = authenticate(username=usern, password=passw)
        if (user is not None):
            login(request, user)

            if prod_id and sub_id:
                return myproducts(request)

            else:
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

    if not "categories" in data["products"][0]:
        message = "Pas assez d'information sur ce produit !"
        category = []
        sub_list = []
        prod_id = ''
        sub_id = ''
        sub_img = ''
        sub_grade = ''
        product="Produit introuvable"

        context = {'product' : product,
                   'message': message}

    else:
        cat_split = data["products"][0]["categories"].split(',')
        #prod_img = data["products"][0]["image_thumb_url"]
        prod_img = data["products"][0]["image_url"]
        #category = cat_split[0]
        category = cat_split
        product = [data["products"][0]["product_name"], category, data["products"][0]["nutrition_grades"], prod_img]

        # Update the Product table if last update was too long ago
        last_update = Update.objects.latest('id')
        print(last_update.LastUpdate)
        #last_update.LastUpdate = last_update.LastUpdate.replace(day=10)
        last_update.save()
        print(last_update.LastUpdate)
        date_now = datetime.date.today()
        delta = date_now - last_update.LastUpdate

        if delta.days >= 10:
            update_tables()
            Update.objects.create(LastUpdate=datetime.date.today())
            print("Update effectué. Last update effectué il y a "+str(delta.days)+" jours.")

        #update_tables()

        #compare to the database

        #sub_list = findsubstitute(product)
        list_results = findsubstitute(product)


        if (list_results ==[]):
            message ='Pas de substitut trouvé pour ce produit.'
            sub_list = []
            prod_id = ''
            sub_id = ''
            sub_img = ''
            sub_grade = ''
        else:
            message = 'Vous pouvez remplacer ce produit par :'
            sub_list = list_results[0]
            prod_id = list_results[1]
            sub_id = list_results[2]
            sub_img = list_results[3]
            sub_grade = list_results[4]


        #display the result



        #tata = Category.objects.create(CategoryName="Tata")
        #tata = Category(CategoryName="Tata")
        #tata.save()

        #categories = Category.objects.all()
        cat_id = Product.objects.filter(ProductName=product[0]).first().CatNum
        category = Category.objects.filter(id=cat_id).first().CategoryName

        context = {'product' : product[0],
                   'categ' : category,
                   'grade' : product[2].upper(),
                   'sublist' : sub_list,
                   'prodid': prod_id,
                   'subid': sub_id,
                   'message' : message,
                   'prodimg': prod_img,
                   'subimg' : sub_img,
                   'subgrade' : sub_grade}

    return render(request, 'searchapp/results.html', context)


def myproducts(request):
    prod_id = request.POST.get('prodid')
    sub_id = request.POST.get('subid')
    user_id = request.user.id

    erase = request.GET.get('erase')

    if (erase=='1'):
        Substitute.objects.all().delete()

    if user_id is None:
        message='Connectez-vous afin de pouvoir sauvegarder ce résultat.'
        page_link = "/searchapp/product"

        context = {'prodid': prod_id,
                   'subid' : sub_id,
                   'message': message}

        return render(request, 'searchapp/login.html', context)

    else:
        #Check if the user has pressed the Save button from the results page
        if (prod_id is None or sub_id is None):
            #prod_id = 'rien du tout'
            #sub_id = 'rien du tout'
            message=''


        #Save the results -> à ajouter check the referer !!!!!!
        else:
            lprod = len(list(Substitute.objects.filter(ProdNum=prod_id, SubNum=sub_id, UserId=user_id)))
            if (lprod == 0):
                Substitute.objects.create(ProdNum=prod_id, SubNum=sub_id, UserId=user_id)
                #prod = Product.objects.filter(id=prod_id).first()
                #sub = Product.objects.filter(id=sub_id).first()
                message = 'Résultat sauvegardé !'
            else:
                message = 'Vous avez déjà enregistré ce substitut pour ce produit.'

        substitutes = list(Substitute.objects.filter(UserId=user_id))
        saved_list = []

        for save in substitutes:
            product = Product.objects.filter(id=save.ProdNum).first().ProductName
            substitute = Product.objects.filter(id=save.SubNum).first().ProductName
            minilist = [product, substitute]

            saved_list.append(minilist)

        context = {'saved' : saved_list,
                   'message' : message}

        return render(request, 'searchapp/myproducts.html', context)

def product(request):
    prod_id = request.POST.get('prodid')
    product = Product.objects.filter(id=prod_id).first()
    categ = Category.objects.filter(id=product.CatNum).first().CategoryName

    context = {'product' : product,
               'categ' : categ}


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
