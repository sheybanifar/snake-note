from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120)
    body = models.TextField(verbose_name='content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60)

    def __str__(self):
        return self.name