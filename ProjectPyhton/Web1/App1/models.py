from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Person(AbstractUser):
    isSeller = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"


class Seller(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    personId = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_commission = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.personId.first_name} {self.personId.last_name}"

    def add_commission(self, amount):
        self.commission += amount
        self.total_commission += amount  # עדכון העמלה הכוללת
        self.save()  # שמירה של המודל לאחר העדכון


class Appartment(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    buildingNum = models.IntegerField()
    floorNum = models.IntegerField()
    roomNum = models.IntegerField()
    condition = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    img = models.ImageField(upload_to="apartments/", blank=True, null=True)
    brokerage = models.BooleanField(default=False)
    sellerId = models.ForeignKey("Seller", on_delete=models.DO_NOTHING)


class Request(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    personId = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    sellerId = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
    apartmentId = models.ForeignKey(Appartment, on_delete=models.CASCADE, null=True)  # קשר לדירה (nullable)
    message = models.CharField(max_length=250)