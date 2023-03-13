
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, FloatField, IntegerField


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass
        



 

class Listings(models.Model):
    title = models.CharField(max_length=64, null = True)
    description =models.CharField(max_length=4096, null = True)
    currentPrice = models.FloatField(null = True)
    category = models.CharField(max_length=64, null = True)
    imageUrl = models.CharField(max_length=4096, null = True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE, null = True)



    def __str__(self):
        if self.currentPrice != None:
            return f"{self.title}: {self.currentPrice}"
        else: 
            return f"{self.title}: Not bid yet "


class Bid(models.Model):
    bidPrice = models.FloatField(null = True)
    buyer= models.ForeignKey(User,on_delete=models.CASCADE, null = True)
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE, null = True)
    

    def __str__(self):

        return f"{self.listing.id} : {self.buyer}: {self.bidPrice}"

class Comment(models.Model):
    comment = models.CharField(max_length=4096, null = True)
    commentator = models.ForeignKey(User,on_delete=models.CASCADE, null = True) 
    auction = models.ForeignKey(Listings,on_delete=models.CASCADE, null = True)

class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null = True) 
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE, null = True)
    
    
    def __str__(self):
        return f"{self.listing}"


        

