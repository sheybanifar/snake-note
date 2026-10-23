from django.db import models
from django.conf import settings

class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    body = models.TextField(verbose_name='content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='notes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'slug'],
                name='unique_note_slug_per_owner')
        ]

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'slug'],
                name='unique_category_slug_per_user'
            )
        ]

    def __str__(self):
        return self.name