from django.db import models


class PublisherModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "publishers"
        app_label = "books"
