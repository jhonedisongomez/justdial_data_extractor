from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class CrawelIssue(models.Model):
    user = models.IntegerField()
    keyword = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    instance_index = models.IntegerField()
    title = models.CharField(max_length=100, default='')
    rating = models.CharField(max_length=100, default='')
    votes = models.CharField(max_length=100, default='')
    contact = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    website = models.CharField(max_length=100, default='')
    others_sites = models.CharField(max_length=500, default='')


    def __str__(self):
        return self.title
