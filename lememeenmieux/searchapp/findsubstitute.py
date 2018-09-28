"""
Here is 'Le même en mieux', a program that enables you
to find a healthy alternative to the food you love.
Based on the data of Openfoodfacts website.
"""

import re
from .models import Category, Product


def findsubstitute(product):
    #Add the product to the db if it doesn't exist
    prod_short = product[0][:40]
    # Check that the product doens't already exist

    results = []

    if (product[0] == '' or product[1] == '' or product[1] is None):
        print("Pas assez d'information sur ce produit")

    else:
        sub_exists = 0
        # Retrieve the French name of the category
        cat_split = product[1]
        r = re.compile("fr*")
        cat_new = filter(r.match, cat_split)
        cat_short = list(cat_new)

        #if (cat_short == []):
        #    cat_fin = cat_split[0]
        #else:
        #    cat_fin = cat_short[0][3:]


        if (cat_short != []):
            cat_fin = cat_short[0][3:]
        else:
            for cat in cat_split:

                if "fr:" in cat:
                    cat_fin = cat[3:]
                else:
                    cat_fin = cat

                if "en:salty-snacks" in cat_fin:
                    cat_fin = "Snacks salés"
                if "en:sugary-snacks" in cat_fin:
                    cat_fin = "Snacks sucrés"
                if (("Pflanzliche Lebensmittel und Getrõnke" in cat_fin) or (
                        "en:plant-based-foods-and-beverages" in cat_fin)):
                    cat_fin = "Aliments et boissons à base de végétaux"
                if "en:beverages" in cat_fin:
                    cat_fin = "Boissons"
                if "en:dairies" in cat_fin:
                    cat_fin = "Produits laitiers"
                if "en:desserts" in cat_fin:
                    cat_fin = "Desserts"
                if "en:fresh-foods" in cat_fin:
                    cat_fin = "Produits Frais"
                if "en:fats" in cat_fin:
                    cat_fin = "Matières grasses"
                #Shortcuts
                if "Jus" in cat_fin:
                    cat_fin = "Boissons"
                if "Confiserie" in cat_fin:
                    cat_fin = "Confiseries"
                if "Confiture" in cat_fin:
                    cat_fin = "Confitures"
                if "Chips" in cat_fin:
                    cat_fin = "Snacks salés"
                if "Chocolats" in cat_fin:
                    cat_fin = "Chocolats"
                if "Yaourts" in cat_fin:
                    cat_fin = "Produits laitiers"
                if "Fromages" in cat_fin:
                    cat_fin = "Fromages"


                try:
                    cat_id = Category.objects.filter(CategoryName=cat_fin)[0].id
                    sub_list = Product.objects.filter(CatNum=cat_id).order_by('Grade')
                    #print("ID de la catégorie: ", cat_id)
                    #print("sub_list", sub_list)

                    candidate_list = []
                    for candidate in sub_list:
                        #clist = list(candidate)
                        #print(clist)
                        print(candidate)
                        # if (clist[1] == prod_choice):
                        if (candidate.Grade == product[2]):
                            break
                        else:
                            candidate_list.append(candidate)
                            sub_exists = 1

                    if sub_exists:
                        #prod_id = Product.objects.filter(ProductName=product[0][:40]).first().id
                        sub_id = Product.objects.filter(ProductName=candidate_list[0].ProductName).first().id
                        sub_img = Product.objects.filter(ProductName=candidate_list[0].ProductName).first().ImageLink
                        sub_grade = Product.objects.filter(ProductName=candidate_list[0].ProductName).first().Grade
                        # return candidate_list
                        #results = [candidate_list, 0, sub_id, sub_img, sub_grade]
                        break

                except IndexError:
                    print("Cette catégorie n'existe pas. ", cat_fin)

                print("Fin du scan de la catégorie ", cat_fin)

        lprod = len(list(Product.objects.filter(ProductName=prod_short)))

        if lprod == 0:
            #Creation of a new product and maybe category

            print("Ajout en cours : - categorie : ", cat_fin, "et produit", prod_short)

            cat_query = Category.objects.filter(CategoryName=cat_fin).first()
            lg = len(list(Category.objects.filter(CategoryName=cat_fin)))
            print("Il y a déjà", lg, "occurrences pour la catégorie", cat_fin)


            if lg == 0:

                last_cat_id = Category.objects.latest('id').id
                new_id = last_cat_id + 1
                Category.objects.create(id=new_id, CategoryName=cat_fin)
                print("Cette catérogie est ajoutée :", cat_fin)

                Product.objects.create(ProductName=prod_short, Grade=product[2], CatNum=new_id,\
                                       ImageLink=product[3][:150], Link=product[4][:150])
                print("Ce produit est ajouté :", prod_short)



            else:
                Product.objects.create(ProductName=prod_short, Grade=product[2],\
                                       CatNum=cat_query.id, ImageLink=product[3][:150], Link=product[4][:150])
                print("Ce produit est ajouté :", prod_short)

        else:
            print("Le produit existe déjà!")


        if not sub_exists:
            pass
        else:
            prod_id = Product.objects.filter(ProductName=prod_short).first().id
            results = [candidate_list, prod_id, sub_id, sub_img, sub_grade.upper()]

    return results
