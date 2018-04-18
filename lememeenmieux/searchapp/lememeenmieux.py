import MySQLdb
import json
import os

"""
Here is 'Le même en mieux', a program that enables you
to find a healthy alternative to the food you love.
Based on the data of Openfoodfacts website.
"""

#Function that clears the console screen
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


#Connection to openfood db (The password will be stored in another file later !!)
db=MySQLdb.connect(user="root",passwd="ocsql",db="openfood")

c=db.cursor()

#Retrieve of DB data as lists
c.execute('SELECT * from categories ORDER BY id;')
cat_tup=c.fetchall()
cat_list=list(cat_tup)

#c.execute('SELECT * from products ORDER BY id;')
#prod_tup=c.fetchall()
#prod_list=list(prod_tup)




#Main loop
stay=1
while (stay):

    cls()
    #Interaction with the user
    print("\n\nLe même en mieux : faites vous plaisir tout en mangeant mieux.\n\n")
    print("Faites votre choix:\n")
    print("1) Rechercher une catégorie")
    print("2) Afficher les recherches sauvegardées")
    print("3) Effacer les recherches sauvegardées")
    print("4) Quitter\n")
    #c.execute("""SELECT (id,CategoryName) FROM Categories""")
    menu = input("Entrez 1, 2, 3 ou 4: ")

    while menu not in ["1","2","3","4"]:
        print("Saisie incorrecte !")
        menu = input("Entrez 1, 2, 3 ou 4: ")

    #Display of the last results of the search for substitutes    
    if (menu == "2"):
        #c.execute("""SELECT ProdNum,SubNum from Substitutes ORDER BY id """)
        #subaslist=list(c.fetchall())
        #print(subaslist)

        c.execute("""SELECT Products.ProductName,Substitutes.ProdNum from Products
                    INNER JOIN Substitutes on Products.id = Substitutes.SubNum
                    ORDER BY Substitutes.id """)
        subaslist=list(c.fetchall())
        #print(subaslist)

        print("Choisissez parmi les produits suivants :")


        sub_id_list=[0]
        new_id_sub=1
        for elt in subaslist:
            #print(" ",eltp[0]," - ",eltp[1])
            c.execute("""SELECT ProductName from Products WHERE id like %s """,(elt[1],))
            prodsub=list(c.fetchone())
            #print(prodsub)
            #print(elt)
            #print(" ",new_id_sub," - ",elt[1],"peut remplacer",elt[0])
            print(" ",new_id_sub," - ",elt[0],"peut remplacer",prodsub[0])
            sub_id_list.append(new_id_sub)
            new_id_sub+=1

        #Loop for the keyboard input
        choice=1000
        while (choice not in sub_id_list):
            print("\nEntrez 0 pour revenir au menu")
            menu_sub = input("Ou entrez le numéro d'une alternative pour avoir plus d'infos : ")
            try:
                choice=int(menu_sub)
            except EOFError as e:
                print("Saisie incorrecte !")
            except ValueError as v:
                print("Saisie incorrecte !")
                        
        
        if choice == 0:
            pass
        else:
            sub_choice = subaslist[choice-1][0]
            c.execute("""SELECT Places,Stores,Link,ProductName from Products WHERE ProductName like %s """,(sub_choice,))
            #print(subaslist)

            infoaslist=list(c.fetchone())
            print("\nNom de l'alternative :",infoaslist[3])
            print("Pays ou Ville :",infoaslist[0])
            print("Lieu de Vente :",infoaslist[1])
            print("Plus d'info ici :",infoaslist[2])


            print("\n\nRevenir au menu principal ?")
            print("1-oui      2-quitter le programme")
            back=input("\nVotre choix : ")
            
            while back not in ["1","2"]:
                print("Saisie incorrecte !")
                back = input("Entrez 1 ou 2 : ")
                
            if (back == "1"):
                pass
            elif (back =="2"):
                stay=0
                
    #Erase of "Substitutes" Table        
    elif (menu == "3"):
        c.execute("""TRUNCATE TABLE Substitutes;""")

    elif (menu == "4"):
        stay=0

    #Display of "Categories" Table
    elif (menu =="1"):
        print("\nChoisissez parmi les catégories suivantes :")


        cat_id_list=[]
        for elt in cat_list:
            print(" ",elt[0]," - ",elt[1])
            cat_id_list.append(elt[0])


        choice=0
        while (choice not in cat_id_list):
            cat_num = input("\nEntrez le numéro d'une catégorie : ")
            try:
                choice=int(cat_num)
            except EOFError as e:
                print("Saisie incorrecte !")
            except ValueError as v:
                print("Saisie incorrecte !")
        
        cat_choice = cat_list[int(cat_num)-1][1]
        print("Votre choix est", cat_choice)


        #c.execute("""SELECT * from products WHERE CategoryName like %s ORDER BY id """,(cat_choice,))
        c.execute("""SELECT * from Products
                    INNER JOIN Categories on products.CatNum = categories.id
                    WHERE Categories.CategoryName like %s ORDER BY products.id """,(cat_choice,))

        prod_tup=c.fetchall()
        prod_list=list(prod_tup)
        #print(prod_list)

        print("\nChoisissez parmi les produits suivants :")

        prod_id_list=[]
        new_id_prod=1
        for eltp in prod_list:
            print(" ",new_id_prod," - ",eltp[1])
            prod_id_list.append(new_id_prod)
            new_id_prod+=1
            

        #print(prod_id_list)


        choice=0
        while (choice not in prod_id_list):
            prod_num = input("\nEntrez le numéro d'un produit : ")
            try:
                choice=int(prod_num)
            except EOFError as e:
                print("Saisie incorrecte !")
            except ValueError as v:
                print("Saisie incorrecte !")

                
        prod_choice = prod_list[int(prod_num)-1][1]
        print("Votre choix est", prod_choice)

        #Calculation of the best substitute
        #c.execute("""SELECT * from products WHERE CategoryName like %s ORDER BY Grade """,(cat_choice,))
        c.execute("""SELECT * from Products
                    INNER JOIN Categories on products.CatNum = categories.id
                    WHERE Categories.CategoryName like %s ORDER BY Grade """,(cat_choice,))

        sub_list=list(c.fetchall())
        #print("Voici la liste des produits :")
        #print(sub_list)

        sub_exists=0
        candidate_list=[]
        for candidate in sub_list:
            clist=list(candidate)
            #print(clist)
            if (clist[1] == prod_choice):
                break
            else:
                candidate_list.append(clist[1])
                sub_exists=1
        if sub_exists:        
            #print("Voici la liste des alternatives :")
            #print(candidate_list)

            print("\nVoici la meilleure alternative à votre produit :")
            print(candidate_list[0])

            #Display of further info on the substitute found
            
            c.execute("""SELECT Places,Stores,Link,id from Products WHERE ProductName like %s """,(candidate_list[0],))
            infoaslist=list(c.fetchone())

            
            print("\nVoulez-vous voir afficher les infos relatives à cette alternative ?")
            moreinfo = input(" 1-Oui 2-Non : ")

            while moreinfo not in ["1","2"]:
                print("Saisie incorrecte !")
                moreinfo = input("Entrez 1 ou 2 : ")
                
            if (moreinfo == "2"):
                pass
            elif (moreinfo =="1"):
                #c.execute("""SELECT Places,Stores,Link from Products WHERE ProductName like %s """,(candidate_list[0],))
                #infoaslist=list(c.fetchone())
                print("\n\nNom de l'alternative :",candidate_list[0])
                print("Pays ou Ville :",infoaslist[0])
                print("Lieu de Vente :",infoaslist[1])
                print("Plus d'info ici :",infoaslist[2])
        
            print("\n\nVoulez-vous sauvegarder ce résultat ? ")
            save = input(" 1-Oui 2-Non : ")

            while save not in ["1","2"]:
                print("Saisie incorrecte !")
                save = input("Entrez 1 ou 2 : ")
                
            if (save == "2"):
                pass
            elif (save =="1"):
                #print("Sauvegarde en cours pour le couple ",prod_choice,"/",candidate_list[0])
                #c.execute("""INSERT INTO Substitutes (ProductName,SubName) VALUES (%s,%s)""",(prod_choice,candidate_list[0],))
            
                c.execute("""SELECT id from Products WHERE ProductName like %s """,(prod_choice,))
                prodid=list(c.fetchone())
                print("produit de substitution",infoaslist)
                
                c.execute("""INSERT INTO Substitutes (ProdNum,SubNum) VALUES (%s,%s)""",(prodid[0],infoaslist[3],))
                print("Alternative sauvegardée ! ")
        else:
            print("\nIl n'y a pas d'alternative saine au produit.")
                
        #Back to main menu or not
        print("\n\nRevenir au menu principal ?")
        print("1-oui      2-quitter le programme")
        back=input("\nVotre choix : ")
        
        while back not in ["1","2"]:
            print("Saisie incorrecte !")
            back = input("Entrez 1 ou 2 : ")
            
        if (back == "1"):
            pass
        elif (back =="2"):
            stay=0
                



db.commit()


