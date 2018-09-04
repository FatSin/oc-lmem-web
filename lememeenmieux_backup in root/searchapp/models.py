from django.db import models

# Create your models here.

class Category(models.Model):
    CategoryName = models.CharField(max_length=40, unique=True)

class Product(models.Model):
    ProductName = models.CharField(max_length=40, unique=True)
    CatNum = models.PositiveSmallIntegerField()
    Places = models.CharField(max_length=40, null=True)
    Stores = models.CharField(max_length=40, null=True)
    Grade = models.CharField(max_length=1, null=True)
    Link = models.CharField(max_length=150, null=True)
    ImageLink = models.CharField(max_length=150, default='https://cdn.pixabay.com/photo/2017/02/14/07/44/cake-2065046_1280.jpg')

class Substitute(models.Model):
    ProdNum = models.PositiveSmallIntegerField()
    SubNum = models.PositiveSmallIntegerField()
    UserId = models.PositiveSmallIntegerField()

class Update(models.Model):
    LastUpdate = models.DateField()
    Comment = models.CharField(max_length=100, null=True)
