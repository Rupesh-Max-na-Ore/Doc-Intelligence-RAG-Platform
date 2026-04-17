from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title