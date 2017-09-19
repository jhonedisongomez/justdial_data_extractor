from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings


class CrawelIssue(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    crawel_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100),])