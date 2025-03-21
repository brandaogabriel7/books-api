from django.db import models

from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel


class BookModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    authors = models.ManyToManyField(AuthorModel, related_name="books")
    publishers = models.ManyToManyField(PublisherModel, related_name="books")
    isbn10 = models.CharField(max_length=10, null=True)
    isbn13 = models.CharField(max_length=13, null=True)
    publish_date = models.DateField(null=True)
    number_of_pages = models.IntegerField(null=True)

    class Meta:
        app_label = "books"
        db_table = "books"
