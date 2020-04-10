from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	image = models.CharField(max_length=500)
	article_link = models.CharField(max_length=500, default='None')
	ingredients = models.TextField()
	text = models.TextField()
	published_date = models.DateTimeField(default=timezone.now())

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title
