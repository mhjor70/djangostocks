from django.db import models

#test change number 2
# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=4)

    def __str__(self):
        return self.ticker
