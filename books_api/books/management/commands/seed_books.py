from django.core.management.base import BaseCommand

import json

from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel

from books.domain.factory.book_factory import book_factory


class Command(BaseCommand):
    help = "Populate the database with books"

    def handle(self, *args, **kwargs):
        try:
            with open("db/books.json") as file:
                books = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON file"))
            return

        for book_data in books:
            author_models = [
                AuthorModel.objects.get_or_create(name=author)[0]
                for author in book_data.get("authors", [])
            ]
            publisher_models = [
                PublisherModel.objects.get_or_create(name=publisher)[0]
                for publisher in book_data.get("publishers", [])
            ]

            book_model, created = BookModel.objects.update_or_create(
                id=book_data.get("id"),
                title=book_data.get("title"),
                subtitle=book_data.get("subtitle", None),
                description=book_data.get("description", None),
                isbn10=book_data.get("isbn10", None),
                isbn13=book_data.get("isbn13", None),
                publish_date=book_data.get("publishDate", None),
                number_of_pages=book_data.get("numberOfPages", None),
            )

            book_model.authors.set(author_models)
            book_model.publishers.set(publisher_models)

            self.stdout.write(
                f"Book {book_model.title} was {'created' if created else 'updated'}"
            )

        self.stdout.write(
            self.style.SUCCESS("Books created or updated successfully")
        )
