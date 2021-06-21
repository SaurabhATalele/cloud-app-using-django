from django.db import models


# Create your models here.
class Meta(models.Model):
    user = models.CharField(max_length=30)
    data = models.BinaryField()

class devs(models.Model):
    username = models.CharField(max_length=50)
    user_sid = models.BinaryField()
    user_password = models.BinaryField()
    date_joined = models.DateTimeField()

class projects(models.Model):
    owner = models.CharField(max_length=50)
    project_name = models.CharField(max_length=50)
    project_id = models.CharField(unique=True,max_length=50)

class slaves(models.Model):
    address = models.CharField(max_length=20)


class storage(models.Model):
    user = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)

    