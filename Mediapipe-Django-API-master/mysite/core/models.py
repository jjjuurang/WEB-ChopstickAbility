from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

#####################################

class User(models.Model):
    username = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)
    email = models.CharField(max_length=100)