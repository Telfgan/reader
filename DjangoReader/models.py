from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=50)


class Translations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="origin_language")
    translating_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="translating_language")
    text = models.TextField()
    date_translating = models.DateField()


