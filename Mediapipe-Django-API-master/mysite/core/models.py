from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

# class tutorial(models.Model):
#     NAME = models.CharField(max_length=200)
#     STEP1 =
#     STEP2 =
#     STEP3 =
#     STEP4 =