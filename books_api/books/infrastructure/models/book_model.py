from django.db import models


class BookModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    authors = models.CharField(max_length=255)
    publishers = models.CharField(max_length=255)
    isbn10 = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    publish_date = models.DateField()
    number_of_pages = models.IntegerField()

    class Meta:
        app_label = "books"
