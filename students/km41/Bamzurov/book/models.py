from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

class Book(models.Model):
	name = models.CharField(max_length=20)
	pub_date = models.DateField(null=True, blank=True)
	author = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class Group(models.Model):
	name = models.CharField(max_length=20)
	owner = models.ForeignKey(User)
	books = models.ManyToManyField(Book)

	def __str__(self):
		return self.name


		
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

# Create your models here.
