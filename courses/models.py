from django.db import models

# Create your models here.
class Beginners(models.Model):
    title = models.CharField(max_length=30)
    titletranslate = models.TextField()
    word = models.TextField()
    meaning = models.TextField()
    audio = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Intermediate(models.Model):
    title = models.CharField(max_length=30)
    titletranslate = models.TextField()
    word = models.TextField()
    meaning = models.TextField()
    audio = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Advance(models.Model):
    title = models.CharField(max_length=30)
    titletranslate = models.TextField()
    word = models.TextField()
    meaning = models.TextField()
    audio = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title

