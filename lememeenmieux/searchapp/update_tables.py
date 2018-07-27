import requests
#import MySQLdb
import json
import re

from .models import Category, Product, Substitute


"""
    Script for the creation and population of Openfood local db's tables,
    from online data. The db must be created (no data necesary) before launching the script.
"""

def update_tables():
    #HTTP Requests To Retrieve the 1st 3 pages of the products sold in France
    req1 = requests.get('https://world.openfoodfacts.org/country/france.json')
    req2 = requests.get('https://world.openfoodfacts.org/country/france/2.json')
    req3 = requests.get('https://world.openfoodfacts.org/country/france/3.json')
    req4 = requests.get('https://world.openfoodfacts.org/country/france/4.json')
    req5 = requests.get('https://world.openfoodfacts.org/country/france/5.json')

    #Conversion of HTTP content into json, and utf8-decoding to avoid charset conflicts due to FR characters
    data1 = json.loads(req1.content.decode('utf-8'))
    data2 = json.loads(req2.content.decode('utf-8'))
    data3 = json.loads(req3.content.decode('utf-8'))
    data4 = json.loads(req4.content.decode('utf-8'))
    data5 = json.loads(req5.content.decode('utf-8'))

    data = [data1, data2, data3, data4, data5]
    #data = [data1]

    #Connection to openfood db (The password will be stored in another file later !!)
    #db=MySQLdb.connect(user="root",passwd="ocsql",db="openfood")

    #c=db.cursor()

    """
    #Decoding to avoid charset conflicts due to FR characters, again
    #db.set_character_set('utf8')
    #c.execute('SET NAMES utf8;')
    #c.execute('SET CHARACTER SET utf8;')
    #c.execute('SET character_set_connection=utf8;')
    """

    #Erase the existing tables
    #c.execute("""DROP TABLE IF EXISTS Substitutes """)
    #c.execute("""DROP TABLE IF EXISTS Products """)
    #c.execute("""DROP TABLE IF EXISTS Categories """)


    #c.execute("""ALTER TABLE Products
    #           DROP FOREIGN KEY prod_k""")
    """
    c.execute('TRUNCATE TABLE Substitutes;')
    c.execute('TRUNCATE TABLE  Products;')
    c.execute('TRUNCATE TABLE  Categories;')
    """
    #c.execute("""ALTER TABLE Products
    #            ADD CONSTRAINT prod_k FOREIGN KEY (CatNum) REFERENCES Categories (id)""")
    #c.execute("""ALTER TABLE Substitutes
    #            ADD CONSTRAINT sub_k FOREIGN KEY (ProdNum) REFERENCES Products (id)""")

    #Creation of Categories and Products tables -> handled by .sql script
    #c.execute("""CREATE TABLE IF NOT EXISTS Categories (
    #    id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
    #    CategoryName VARCHAR(40) UNIQUE NOT NULL)""")

    #c.execute("""CREATE TABLE IF NOT EXISTS Products (
     #   id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      #  ProductName VARCHAR(40) UNIQUE NOT NULL,
       # CategoryName VARCHAR(40) NOT NULL,
    #    Places VARCHAR(40),
    #    Stores VARCHAR(40),
    #    Grade VARCHAR(1) NOT NULL)""")

    #c.execute("""CREATE TABLE IF NOT EXISTS Substitutes (
    #    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #    ProductName VARCHAR(40) NOT NULL,
    #    SubName VARCHAR(40) NOT NULL,
    #    purchase_places VARCHAR(40),
    #    stores VARCHAR(40))""")

    #c.execute("""CREATE TABLE IF NOT EXISTS Products (
    #    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #    ProductName VARCHAR(40) UNIQUE NOT NULL,
    #    CategoryName VARCHAR(40) NOT NULL,
    #    Places VARCHAR(40),
    #    Stores VARCHAR(40),
    #    Grade VARCHAR(1),
    #    CONSTRAINT fk_catname
    #      FOREIGN KEY (CategoryName)
    #      REFERENCES Categories(CategoryName))""")

    Category.objects.all().delete()
    Product.objects.all().delete()
    Substitute.objects.all().delete()


    #Population of the tables with HTTP content
    cat_id=1
    for element in data:
        for entry in element["products"]:
            #Check the presence of critical keys/columns
            if ("categories" in entry.keys() and "product_name" in entry.keys() and "nutrition_grade_fr" in entry.keys()):
                if (entry["categories"] == '' or entry["product_name"] == ''):
                    #print("Rejeté car nul : - categorie : ",entry["categories"],"et produit",entry["product_name"])
                    pass
                    #print("cette cat est vide!")
                else:

                    prod_short = entry["product_name"][:40]

                    #Check that the product doens't already exist
                    lprod = len(list(Product.objects.filter(ProductName=prod_short)))

                    if (lprod==0):

                        #Retrieve the French name of the category
                        cat_split = entry["categories"].split(',')
                        r=re.compile("fr*")
                        cat_new=filter(r.match,cat_split)
                        cat_short=list(cat_new)
                        if (cat_short == []):
                            cat_fin=cat_split[0]
                        else:
                            cat_fin=cat_short[0][3:]

                        cat_fin=cat_fin[:40]

                        if (cat_fin == "en:salty-snacks"):
                            cat_fin="Snacks salés"
                        if (cat_fin == "en:sugary-snacks"):
                            cat_fin="Snacks sucrés"
                        if ((cat_fin == "Pflanzliche Lebensmittel und Getrõnke") or (cat_fin == "en:plant-based-foods-and-beverages")):
                            cat_fin="Aliments et boissons à base de végétaux"
                        if (cat_fin == "en:beverages"):
                            cat_fin="Boissons"
                        if (cat_fin == "en:dairies"):
                            cat_fin = "Produits laitiers"
                        if (cat_fin == "en:desserts"):
                            cat_fin = "Desserts"



                        print("Ajout en cours : - categorie : ",cat_fin,"et produit",prod_short)

                        #Mysql version"""
                        #c.execute("""SELECT id FROM Categories WHERE CategoryName like %s""", (cat_fin,))
                        #cat_list=list(c.fetchall())
                        #lg=len(cat_list)
                        #print(cat_list)"""

                        cat_query = Category.objects.filter(CategoryName=cat_fin).first()
                        lg = len(list(Category.objects.filter(CategoryName=cat_fin)))
                        print("Il y a déjà", lg,"occurrences pour la catégorie",cat_fin)

                        #Category.objects.create(id=cat_id, CategoryName=cat_fin)

                        if (lg==0):
                            """
                            Mysql db style
                            """
                            #c.execute("""INSERT IGNORE INTO Categories (id,CategoryName) VALUES (%s,%s)""", (cat_id,cat_fin,))

                            #Import information and location, if they exist
                            #if ("stores" in entry.keys() and "purchase_places" and "url" in entry.keys()):
                                ##c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade,Places,Stores,Link,CatNum) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (prod_short,cat_fin,entry["nutrition_grade_fr"],entry["purchase_places"],entry["stores"],entry["url"],cat_id))
                                #c.execute("""INSERT IGNORE INTO Products (ProductName,Grade,Places,Stores,Link,CatNum) VALUES (%s,%s,%s,%s,%s,%s)""", (prod_short,entry["nutrition_grade_fr"],entry["purchase_places"],entry["stores"],entry["url"],cat_id))

                                #print("stores, place et url :", entry["stores"], entry["purchase_places"], entry["url"])
                            #else:
                               # #c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade,CatNum) VALUES (%s,%s,%s,%s)""", (prod_short,cat_fin,entry["nutrition_grade_fr"],cat_id,))
                                #c.execute("""INSERT IGNORE INTO Products (ProductName,Grade,CatNum) VALUES (%s,%s,%s)""", (prod_short,entry["nutrition_grade_fr"],cat_id,))

                            #print("Ce produit est ajouté :", entry["product_name"])

                            #cat_id+=1

                            Category.objects.create(id=cat_id, CategoryName=cat_fin)

                            # Import information and location, if they exist
                            if ("stores" in entry.keys() and "purchase_places" in entry.keys() and "url" in entry.keys()):
                                Product.objects.create(ProductName=prod_short, Grade=entry["nutrition_grade_fr"], Places=entry["purchase_places"][40:], Stores=entry["stores"][40:], Link=entry["url"][50:], CatNum=cat_id)
                            else:
                                Product.objects.create(ProductName=prod_short, Grade=entry["nutrition_grade_fr"], CatNum=cat_id)
                            print("Ce produit est ajouté :", entry["product_name"])

                            cat_id+=1


                        else:

                            """
                            Mysql db style
                            """
                            #if ("stores" in entry.keys() and "purchase_places" and "url" in entry.keys()):
                                ##c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade,Places,Stores,Link,CatNum) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (prod_short,cat_fin,entry["nutrition_grade_fr"],entry["purchase_places"],entry["stores"],entry["url"],cat_list[0]))
                                #c.execute("""INSERT IGNORE INTO Products (ProductName,Grade,Places,Stores,Link,CatNum) VALUES (%s,%s,%s,%s,%s,%s)""", (prod_short,entry["nutrition_grade_fr"],entry["purchase_places"],entry["stores"],entry["url"],cat_list[0]))

                                #print("stores, place et url :", entry["stores"], entry["purchase_places"], entry["url"])
                            #else:
                                ##c.execute("""INSERT IGNORE INTO Products (ProductName,Grade,CatNum) VALUES (%s,%s,%s)""", (prod_short,entry["nutrition_grade_fr"],cat_list[0],))
                                ##c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade,CatNum) VALUES (%s,%s,%s,%s)""", (prod_short,cat_fin,entry["nutrition_grade_fr"],cat_list[0],))
                                #c.execute("""INSERT IGNORE INTO Products (ProductName,Grade,CatNum) VALUES (%s,%s,%s)""", (prod_short,entry["nutrition_grade_fr"],cat_list[0],))

                            #print("Ce produit est ajouté :", entry["product_name"])

                            if ("stores" in entry.keys() and "purchase_places" in entry.keys() and "url" in entry.keys()):
                                if "image_thumb_url" in entry.keys():
                                    Product.objects.create(ProductName=prod_short, Grade=entry["nutrition_grade_fr"], Places=entry["purchase_places"][40:], Stores=entry["stores"][40:], Link=entry["url"][50:], CatNum=cat_query.id, ImageLink=["image_thumb_url"][150:])
                                else:
                                    Product.objects.create(ProductName=prod_short, Grade=entry["nutrition_grade_fr"], Places=entry["purchase_places"][40:], Stores=entry["stores"][40:], Link=entry["url"][50:], CatNum=cat_query.id)
                                print("stores, place et url :", entry["stores"], entry["purchase_places"], entry["url"])
                            else:
                                if "image_thumb_url" in entry.keys():
                                    Product.objects.create(ProductName=prod_short, Grade=entry["nutrition_grade_fr"], CatNum=cat_query.id, ImageLink=["image_thumb_url"][150:])
                                else:
                                    Product.objects.create(ProductName=prod_short, Grade=entry["nutrition_grade_fr"],
                                                           CatNum=cat_query.id)
                                print("Ce produit est ajouté :", entry["product_name"])

                    else:
                        print("Le produit existe déjà!")
            else:
                print("Keys pas bonnes!!")

    print("Update terminé.")
    return "ok"