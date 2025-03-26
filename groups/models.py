from django.db import models
from django.utils.text import slugify
# Create your models here.


import misaka
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django import template
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(blank=True, default='', editable=False)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генеруємо slug на основі імені групи
        self.slug = slugify(self.name)
        # Конвертуємо текст опису до HTML, якщо використовується misaka
        self.description_html = misaka.html(self.description)
        # Викликаємо метод збереження батьківського класу
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='membership', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')


