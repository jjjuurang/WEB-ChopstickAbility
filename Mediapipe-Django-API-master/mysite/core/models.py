from django.conf import settings
from django.db import models



class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Tutorial(models.Model):
    NAME = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="username", primary_key=True)
    STEP1 = models.IntegerField(default=0)
    STEP2 = models.IntegerField(default=0)
    STEP3 = models.IntegerField(default=0)
    STEP4 = models.IntegerField(default=0)
