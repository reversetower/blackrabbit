#models.py
from django.db import models

class ForSystem(models.Model):
    check_time = models.CharField(max_length=20, blank=True)

    def __main__(self):
        return self.check_time

class TrcTech(models.Model):
    news_source = models.CharField(max_length=10, blank=True)
    news_cate = models.CharField(max_length=10, blank=True)
    news_title = models.CharField(max_length=80, blank=False)
    news_date = models.CharField(max_length=20, blank=True)
    news_url = models.URLField()

    def __str__(self):
        return self.news_title
