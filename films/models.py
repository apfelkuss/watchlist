from django.db import models
from django.urls import reverse

from model_utils import Choices


class Film(models.Model):
    STATUSES = Choices(("to_watch", "хочу посмотреть"), ("completed", "просмотренное"))

    kinopoisk_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    title_original = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=50)
    poster = models.URLField()
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=200)
    scriptwriter = models.CharField(max_length=200)
    actors = models.CharField(max_length=200)
    plot = models.TextField(max_length=1000)
    length = models.PositiveSmallIntegerField()
    status = models.CharField(choices=STATUSES, default=STATUSES.to_watch, max_length=9)
    edit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " (" + str(self.year) + ")"

    def get_absolute_url(self):
        return reverse("films:detail", kwargs={"pk": self.pk})
