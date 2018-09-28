"""
This file describes the views of the Django site lememenmieux.herokuapp.com.
"""


import json
import datetime

import requests
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404

from .models import Category, Product, Substitute, Update
from .update_tables import update_tables
from .findsubstitute import findsubstitute


def index(request):
    """
    Actions triggered when / is called. Also manages authentication.
    """
    usern = request.POST.get('username')
    passw = request.POST.get('password')
    create_user = request.POST.get('createuser')
    prod_id = request.POST.get('prodid')
    sub_id = request.POST.get('subid')


    if create_user:
        if (usern is not None and passw is not None):
            new_user = User.objects.create_user(usern, '', passw)
            #message_bis = new_user.username

    if (usern is not None and passw is not None):
        user = authenticate(username=usern, password=passw)
        if user is not None:
            login(request, user)

            if prod_id and sub_id:
                return myproducts(request)


            context = {'username':usern,
                       'authenticated':1}
            return render(request, 'searchapp/index.html', context)

        message = 'Connexion impossible'
        context = {'message':message}
        return render(request, 'searchapp/login.html', context)


    if request.user.is_authenticated:
        usern = request.user.username
        context = {'username':usern,
                   'authenticated':1}
        return render(request, 'searchapp/index.html', context)

    return render(request, 'searchapp/index.html')


def results(request):
    """
    Actions triggered when a product is searched for on Open Food Facts API.
    Displays an alternative, healthier product if it exists in the local DB.
    """

    query = request.GET.get('query')
    #retrieve the query from the search bar

    try:
        req = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms="+\
                           query+"&countries=en:france&search_simple=1&action=process&json=1")
        data = json.loads(req.content.decode('utf-8'))

    except:
        data = {
            "skip": 0,
            "page_size": "0",
            "page": 1,
            "products": [
                {"":""
                }
                ],
            "count": 0
            }

    if data["products"] == []:
        #message = "Désolé, ce produit n'existe pas dans la base !"
        #product_result = "Produit introuvable"

        #context = {'product': product_result,
        #           'message': message,
        #           'prodimg': '/static/searchapp/img/plate.png'}

        #return render(request, 'searchapp/404.html', context)
        raise Http404("Produit introuvable")

    elif not "categories" in data["products"][0]:
        #message = "Pas assez d'information sur ce produit !"
        #product = "Produit introuvable"

        #context = {'product' : product,
        #           'message': message,
        #           'prodimg': '/static/searchapp/img/plate.png'}

        #return render(request, 'searchapp/404.html', context)
        raise Http404("Produit introuvable")

    else:
        categories = data["products"][0]["categories"].split(',')
        #prod_img = data["products"][0]["image_thumb_url"]
        prod_img = data["products"][0]["image_url"]
        product = [data["products"][0]["product_name"], categories,\
                   data["products"][0]["nutrition_grades"], prod_img, data["products"][0]["url"]]


        # Update the Product table if last update was too long ago
        try:
            last_update = Update.objects.latest('id')
            print(last_update.LastUpdate)
            #last_update.LastUpdate = last_update.LastUpdate.replace(day=10)
            last_update.save()
            print(last_update.LastUpdate)
        except:
            last_update = Update.objects.create(LastUpdate="2018-01-01")

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


        if list_results == []:
            message = 'Pas de substitut trouvé pour ce produit.'
            sub_list = []
            prod_id = Product.objects.filter(ProductName=product[0][:40]).first().id
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
    """
    Displays all the products & substitutes saved by an authenticated user.
    """
    prod_id = request.POST.get('prodid')
    sub_id = request.POST.get('subid')
    user_id = request.user.id

    erase = request.GET.get('erase')

    if erase == '1':
        Substitute.objects.all().delete()

    if user_id is None:
        message = 'Connectez-vous afin de pouvoir sauvegarder vos recherches.'
        #page_link = "/searchapp/product"

        context = {'prodid': prod_id,
                   'subid' : sub_id,
                   'message': message}

        return render(request, 'searchapp/login.html', context)

    print(prod_id)
    print(sub_id)
    #Check if the user has pressed the Save button from the results page
    if (prod_id is None or sub_id is None or prod_id == "None" or sub_id == "None"):
        #prod_id = 'rien du tout'
        #sub_id = 'rien du tout'
        message = ''


    #Save the results -> à ajouter check the referer !!!!!!
    else:
        lprod = len(list(Substitute.objects.filter(ProdNum=prod_id,\
                                                   SubNum=sub_id, UserId=user_id)))
        if lprod == 0:
            Substitute.objects.create(ProdNum=prod_id, SubNum=sub_id, UserId=user_id)
            #prod = Product.objects.filter(id=prod_id).first()
            #sub = Product.objects.filter(id=sub_id).first()
            message = 'Résultat sauvegardé !'
        else:
            message = 'Vous avez déjà enregistré ce substitut pour ce produit.'

    substitutes = list(Substitute.objects.filter(UserId=user_id))
    saved_list = []

    for save in substitutes:
        product = Product.objects.filter(id=save.ProdNum).first()
        substitute = Product.objects.filter(id=save.SubNum).first()
        minilist = [product.ProductName, substitute.ProductName, save.ProdNum,\
                    save.SubNum, product.ImageLink, substitute.ImageLink]
        saved_list.append(minilist)

    context = {'saved' : saved_list,
               'message' : message}

    return render(request, 'searchapp/myproducts.html', context)

def product(request):
    """
    Displays the detailed information of a product.
    """
    prod_id = request.POST.get('prodid')

    try:
        prod = Product.objects.filter(id=prod_id).first()
        categ = Category.objects.filter(id=prod.CatNum).first().CategoryName

        if prod.Grade == 'a':
            img_score = "score_a.jpg"
        elif prod.Grade == 'b':
            img_score = "score_b.jpg"
        elif prod.Grade == 'c':
            img_score = "score_c.jpg"
        elif prod.Grade == 'd':
            img_score = "score_d.jpg"
        elif prod.Grade == 'e':
            img_score = "score_e.jpg"

        if not prod.Stores:
            if not prod.Places:
                message = "Il n'y a pas de lieu de vente connu pour ce produit."
            else:
                message = "Vous pouvez-vous procurer ce produit ici : "+prod.Places
        else:
            message = "Vous pouvez-vous procurer ce produit ici : "+prod.Places+",\
             "+prod.Stores

        context = {'product': prod,
                   'categ': categ,
                   'message': message,
                   'scoreimg': img_score}

    except:
        #404 error page
        return render(request, 'searchapp/404.html')
        #raise Http404("Produit introuvable")
    return render(request, 'searchapp/product.html', context)

def myaccount(request):
    """
    Access to an authenticated user's account page.
    """
    update_pass = request.POST.get('updatepass')
    new_passw = request.POST.get('password')

    message = ''

    if request.user.is_authenticated:
        usern = request.user.username
        authenticated = request.user.is_authenticated

        if update_pass is not None and new_passw is not None:
            user_obj = User.objects.get(username=usern)
            user_obj.set_password(new_passw)
            user_obj.save()
            user = authenticate(username=usern, password=new_passw)
            if user is not None:
                login(request, user)

            message = "Mot de passe modifié ! "

        context = {'username': usern,
                   'authenticated': authenticated,
                   'message' : message}



        return render(request, 'searchapp/myaccount.html', context)

    #authenticated = request.user.is_authenticated
    #usern = ''
    return render(request, 'searchapp/login.html')

def dologin(request):
    """
    Displays the login page.
    """
    return render(request, 'searchapp/login.html')


def dologout(request):
    """
    Logs an authenticated user out.
    """
    logout(request)
    return render(request, 'searchapp/index.html')

def legalnotice(request):
    """
    Displays the legal notices.
    """
    return render(request, 'searchapp/legalnotice.html')
