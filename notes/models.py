from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120)
    body = models.TextField(verbose_name='content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)