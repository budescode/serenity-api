from django.db import models

class Beginner(models.Model):
	word = models.TextField()
	meaning = models.TextField()
	audio = models.FileField()

class Intermediate(models.Model):
	word = models.TextField()
	meaning = models.TextField()
	audio = models.FileField()

class Advanced(models.Model):
	word = models.TextField()
	meaning = models.TextField()
	audio = models.FileField()