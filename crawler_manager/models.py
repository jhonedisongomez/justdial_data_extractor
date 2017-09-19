from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings



class CrawelIssue(models.Model):
    keyword = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    crawel_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100),])

    instance_index = models.IntegerField()
    title = models.CharField(max_length=100, default='')
    rating = models.CharField(max_length=100, default='')
    votes = models.CharField(max_length=100, default='')
    contact = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    website = models.CharField(max_length=100, default='')

    # @classmethod
    # def create(cls, keyword, city_name, crawel_number, instance_index, title, rating, votes, contact, address, website):
    #     issue = cls(keyword=keyword,
    #                 city_name = city_name,
    #                 crawel_number = crawel_number,
    #                 instance_index = instance_index,
    #                 title = title,
    #                 rating = rating,
    #                 votes = votes,
    #                 contact = contact,
    #                 address = address,
    #                 website = website,
    #     )
    #     return issue