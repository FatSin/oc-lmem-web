import re
from .models import Category, Product, Substitute

"""
Here is 'Le même en mieux', a program that enables you
to find a healthy alternative to the food you love.
Based on the data of Openfoodfacts website.
"""

def findsubstitute(product):
    #Add the product to the db if it doesn't exist
    prod_short = product[0][:40]
    # Check that the product doens't already exist
    lprod = len(list(Product.objects.filter(ProductName=prod_short)))

    if (lprod == 0):
        if (product[0] == '' or product[1] == ''):
            # print("Rejeté car nul : - categorie : ",entry["categories"],"et produit",entry["product_name"])
            print("Pas assez d'information sur ce produit")

        else:
            # Retrieve the French name of the category
            cat_split = product[1]
            r = re.compile("fr*")
            cat_new = filter(r.match, cat_split )
            cat_short = list(cat_new)
            if (cat_short == []):
                cat_fin = cat_split[0]
            else:
                cat_fin = cat_short[0][3:]

            cat_fin = cat_fin[:40]

            if (cat_fin == "en:salty-snacks"):
                cat_fin = "Snacks salés"
            if (cat_fin == "en:sugary-snacks"):
                cat_fin = "Snacks sucrés"
            if ((cat_fin == "Pflanzliche Lebensmittel und Getrõnke") or (
                    cat_fin == "en:plant-based-foods-and-beverages")):
                cat_fin = "Aliments et boissons à base de végétaux"
            if (cat_fin == "en:beverages"):
                cat_fin = "Boissons"
            if (cat_fin == "en:dairies"):
                cat_fin = "Produits laitiers"
            if (cat_fin == "en:desserts"):
                cat_fin = "Desserts"

            print("Ajout en cours : - categorie : ", cat_fin, "et produit", prod_short)

            cat_query = Category.objects.filter(CategoryName=cat_fin).first()
            lg = len(list(Category.objects.filter(CategoryName=cat_fin)))
            print("Il y a déjà", lg, "occurrences pour la catégorie", cat_fin)

            if (lg == 0):

                last_cat_id = Category.objects.latest('id').id
                new_id = last_cat_id + 1
                Category.objects.create(id=new_id, CategoryName=cat_fin)
                print("Cette catérogie est ajoutée :", cat_fin)

                Product.objects.create(ProductName=prod_short, Grade=product[2], CatNum=new_id, ImageLink=product[3][150:])
                print("Ce produit est ajouté :", prod_short)



            else:
                Product.objects.create(ProductName=prod_short, Grade=product[2],
                                           CatNum=cat_query.id, ImageLink=product[3][150:])
                print("Ce produit est ajouté :", prod_short)

    else:
        print("Le produit existe déjà!")


    try:
        cat_id = Category.objects.filter(CategoryName=product[1][0])[0].id
    except IndexError:
        print("Cette catégorie n'existe pas.")
        return []

    sub_list = Product.objects.filter(CatNum=cat_id).order_by('Grade')

    sub_exists = 0
    candidate_list = []
    for candidate in sub_list:
        #clist = list(candidate)
        # print(clist)
        #if (clist[1] == prod_choice):
        if (candidate.Grade == product[2]):
            break
        else:
            candidate_list.append(candidate)
            sub_exists = 1

    if not sub_exists:
        return []
    else:
        prod_id = Product.objects.filter(ProductName=product[0][:40]).first().id
        sub_id = Product.objects.filter(ProductName=candidate_list[0].ProductName).first().id
        sub_img = Product.objects.filter(ProductName=candidate_list[0].ProductName).first().ImageLink
        sub_grade = Product.objects.filter(ProductName=candidate_list[0].ProductName).first().Grade
        #return candidate_list
        return [candidate_list, prod_id, sub_id, sub_img, sub_grade]
