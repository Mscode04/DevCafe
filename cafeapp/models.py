from django.db import models

# Create your models here.
class MainItem(models.Model):
    productName = models.CharField(max_length=200)
    Discription = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    image=models.ImageField(upload_to='items_media',null=True,blank=True)
    def __str__(self):
        return '{}'.format(self.productName)