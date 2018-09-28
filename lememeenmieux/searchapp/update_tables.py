"""
This function updates the tables Categories, Products and Substitutes, depending on
the date of the previous update. The table Products and Categories are populated with
data from Open Food Facts database. While The substitutes table is flushed.
"""

import json
import re

import requests

from .models import Category, Product, Substitute


def update_tables():
    """
    Main and single function
    """

    #HTTP Requests To Retrieve the 1st 3 pages of the products sold in France
    req1 = requests.get('https://world.openfoodfacts.org/country/france.json')
    req2 = requests.get('https://world.openfoodfacts.org/country/france/2.json')
    req3 = requests.get('https://world.openfoodfacts.org/country/france/3.json')
    req4 = requests.get('https://world.openfoodfacts.org/country/france/4.json')
    req5 = requests.get('https://world.openfoodfacts.org/country/france/5.json')

    #Conversion of HTTP content into json, and utf8-decoding to avoid
    # charset conflicts due to FR characters
    data1 = json.loads(req1.content.decode('utf-8'))
    data2 = json.loads(req2.content.decode('utf-8'))
    data3 = json.loads(req3.content.decode('utf-8'))
    data4 = json.loads(req4.content.decode('utf-8'))
    data5 = json.loads(req5.content.decode('utf-8'))

    data = [data1, data2, data3, data4, data5]

    Category.objects.all().delete()
    Product.objects.all().delete()
    Substitute.objects.all().delete()

    #Population of the tables with HTTP content
    cat_id = 1
    for element in data:
        for entry in element["products"]:
            #Check the presence of critical keys/columns
            if ("categories" in entry.keys() and
                    "product_name" in entry.keys() and
                    "nutrition_grade_fr" in entry.keys()):
                if (entry["categories"] == '' or entry["product_name"] == ''):
                    #print("Rejeté car nul : - categorie : ",entry["categories"],"et produit",entry["product_name"])
                    pass
                    #print("cette cat est vide!")
                else:

                    prod_short = entry["product_name"][:40]

                    #Check that the product doens't already exist
                    lprod = len(list(Product.objects.filter(ProductName=prod_short)))

                    if lprod == 0:

                        #Retrieve the French name of the category
                        cat_split = entry["categories"].split(',')
                        reg = re.compile("fr*")
                        cat_new = filter(reg.match, cat_split)
                        cat_short = list(cat_new)
                        if cat_short == []:
                            cat_fin = cat_split[0]
                        else:
                            cat_fin = cat_short[0][3:]

                        cat_fin = cat_fin[:40]

                        if ("en:salty-snacks" in cat_fin):
                            cat_fin = "Snacks salés"
                        if ("en:sugary-snacks" in cat_fin):
                            cat_fin = "Snacks sucrés"
                        if (("Pflanzliche Lebensmittel und Getrõnke" in cat_fin) or (
                                "en:plant-based-foods-and-beverages" in cat_fin)):
                            cat_fin = "Aliments et boissons à base de végétaux"
                        if ("en:beverages" in cat_fin):
                            cat_fin = "Boissons"
                        if ("en:dairies" in cat_fin):
                            cat_fin = "Produits laitiers"
                        if ("en:desserts" in cat_fin):
                            cat_fin = "Desserts"
                        if ("en:fresh-foods" in cat_fin):
                            cat_fin = "Produits Frais"
                        if ("en:fats" in cat_fin):
                            cat_fin = "Matières grasses"
                        # Shortcuts
                        if ("Jus" in cat_fin):
                            cat_fin = "Boissons"
                        if ("Confiserie" in cat_fin):
                            cat_fin = "Confiseries"
                        if ("Confiture" in cat_fin):
                            cat_fin = "Confitures"
                        if ("Chips" in cat_fin):
                            cat_fin = "Snacks salés"
                        if ("Chocolats" in cat_fin):
                            cat_fin = "Chocolats"
                        if ("Yaourts" in cat_fin):
                            cat_fin = "Produits laitiers"
                        if ("Fromages" in cat_fin):
                            cat_fin = "Fromages"

                        print("Ajout en cours : - categorie : ", cat_fin, "et produit", prod_short)

                        cat_query = Category.objects.filter(CategoryName=cat_fin).first()
                        prod_in_cat = len(list(Category.objects.filter(CategoryName=cat_fin)))
                        print("Il y a déjà", prod_in_cat, "occurrences pour la catégorie", cat_fin)

                        #Category.objects.create(id=cat_id, CategoryName=cat_fin)

                        if prod_in_cat == 0:

                            Category.objects.create(id=cat_id, CategoryName=cat_fin)

                            # Import information and location, if they exist
                            if ("stores" in entry.keys() and "purchase_places" in entry.keys() and "url" in entry.keys()):
                                if "image_url" in entry.keys():
                                    Product.objects.create(ProductName=prod_short,
                                                           Grade=entry["nutrition_grade_fr"],
                                                           Places=entry["purchase_places"][:40],
                                                           Stores=entry["stores"][:40],
                                                           Link=entry["url"][:150],
                                                           CatNum=cat_id, ImageLink=entry["image_url"][:150])
                                else:
                                    Product.objects.create(ProductName=prod_short,
                                                           Grade=entry["nutrition_grade_fr"],
                                                           Places=entry["purchase_places"][:40],
                                                           Stores=entry["stores"][:40],
                                                           Link=entry["url"][:150],
                                                           CatNum=cat_id, ImageLink="/static/searchapp/img/logo.png")
                            else:
                                if "image_url" in entry.keys():
                                    Product.objects.create(ProductName=prod_short,
                                                           Grade=entry["nutrition_grade_fr"],
                                                           CatNum=cat_id,
                                                           ImageLink=entry["image_url"][:150],
                                                           Link=entry["url"][:150])
                                else:
                                    Product.objects.create(ProductName=prod_short,
                                                           Grade=entry["nutrition_grade_fr"],
                                                           CatNum=cat_id,
                                                           ImageLink="/static/searchapp/img/logo.png",
                                                           Link=entry["url"][:150])
                            print("Ce produit est ajouté :", entry["product_name"])

                            cat_id += 1


                        else:
                            if ("stores" in entry.keys() and "purchase_places" in entry.keys() and "url" in entry.keys()):
                                if "image_url" in entry.keys():
                                    Product.objects.create(ProductName=prod_short,\
                                                           Grade=entry["nutrition_grade_fr"],\
                                                           Places=entry["purchase_places"][:40],\
                                                           Stores=entry["stores"][:40],\
                                                           Link=entry["url"][:150],\
                                                           CatNum=cat_query.id,\
                                                           ImageLink=entry["image_url"][:150])
                                else:
                                    Product.objects.create(ProductName=prod_short,\
                                                           Grade=entry["nutrition_grade_fr"],\
                                                           Places=entry["purchase_places"][:40],\
                                                           Stores=entry["stores"][:40],\
                                                           Link=entry["url"][:150],\
                                                           CatNum=cat_query.id,\
                                                           ImageLink="/static/searchapp/img/logo.png")
                                print("stores, place et url :", entry["stores"], entry["purchase_places"], entry["url"])
                            else:
                                if "image_url" in entry.keys():
                                    Product.objects.create(ProductName=prod_short,\
                                                           Grade=entry["nutrition_grade_fr"],\
                                                           CatNum=cat_query.id,\
                                                           ImageLink=entry["image_url"][:150])
                                else:
                                    Product.objects.create(ProductName=prod_short,\
                                                           Grade=entry["nutrition_grade_fr"],
                                                           CatNum=cat_query.id,
                                                           ImageLink="/static/searchapp/img/logo.png")
                                print("Ce produit est ajouté :", entry["product_name"])

                    else:
                        print("Le produit existe déjà!")
            else:
                print("Keys pas bonnes!!")

    print("Update terminé.")
    return "ok"
