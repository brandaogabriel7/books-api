from django.db import models


class AuthorModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "authors"
        app_label = "books"
