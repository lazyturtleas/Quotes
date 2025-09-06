from django.db import models

GENRE_CHOICES = [
    ("Книга", "Книга"),
    ("Фильм", "Фильм"),
    ("Музыка", "Музыка"),
    ("Цитаты реально-существующих", "Цитаты реально-существующих"),
]

class Quote(models.Model):
    text = models.TextField(unique=True)
    source_name = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    author_name = models.CharField(max_length=100, blank=True)
    weight = models.PositiveIntegerField(default=1)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text[:50]} — {self.author_name or 'Не указан'}"

class SiteStats(models.Model):
    total_visitors = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Всего посетителей: {self.total_visitors}"

    class Meta:
        verbose_name = "Статистика сайта"
        verbose_name_plural = "Статистика сайта"


class SiteStats(models.Model):
    total_visitors = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Всего посетителей: {self.total_visitors}"
