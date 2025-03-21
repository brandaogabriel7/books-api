from django.core.paginator import Paginator
from django.db.models import Q

from datetime import date

from books.domain.repository.book_repository import BookRepository

from books.domain.entity.book import Book


from books.infrastructure.models.book_model import BookModel
from books.infrastructure.models.author_model import AuthorModel
from books.infrastructure.models.publisher_model import PublisherModel

import books.infrastructure.models.book_model_mapper as book_model_mapper


class DjangoBookRepository(BookRepository):

    def __build_query(self, filters: object) -> Q:
        isbn = filters.get("isbn", None)
        if isbn:
            return Q(isbn10=isbn) | Q(isbn13=isbn)

        built_filters = {}
        for key, value in filters.items():
            if key == "title":
                built_filters["title__icontains"] = value
            if key == "subtitle":
                built_filters["subtitle__icontains"] = value
            if key == "description":
                built_filters["description__icontains"] = value
            if key == "authors":
                built_filters["authors__name__in"] = value
            if key == "publishers":
                built_filters["publishers__name__in"] = value
            if key == "publishDate":
                built_filters["publish_date"] = date.fromisoformat(value)
            if key == "numberOfPages":
                built_filters["number_of_pages"] = value

        return Q(**built_filters)

    def list(
        self, page: int = 1, page_size: int = 10, filters: object = {}
    ) -> list[Book]:
        query = self.__build_query(filters)

        filtered_books = BookModel.objects.filter(query).order_by("title")
        paginator = Paginator(filtered_books, page_size)
        books_page = paginator.get_page(page)

        return [
            book_model_mapper.book_entity(book)
            for book in books_page.object_list
        ]

    def get(self, book_id: str) -> Book:
        retrieved_book = BookModel.objects.get(id=book_id)

        return book_model_mapper.book_entity(retrieved_book)

    def create(self, book: Book) -> Book:
        new_book = BookModel.objects.create(
            id=book.id,
            title=book.title,
            subtitle=book.subtitle,
            description=book.description,
            isbn10=book.isbn10.value if book.isbn10 else None,
            isbn13=book.isbn13.value if book.isbn13 else None,
            publish_date=(
                date.fromisoformat(book.publishDate.value)
                if book.publishDate is not None
                else None
            ),
            number_of_pages=book.numberOfPages,
        )

        author_instances = [
            AuthorModel.objects.get_or_create(name=author)[0]
            for author in book.authors
        ]

        publisher_instances = [
            PublisherModel.objects.get_or_create(name=publisher)[0]
            for publisher in book.publishers
        ]

        new_book.authors.set(author_instances)
        new_book.publishers.set(publisher_instances)

        created_book = book_model_mapper.book_entity(new_book)

        return created_book

    def update(self, book_id: str, book: Book) -> Book:
        existing_book = BookModel.objects.get(id=book_id)

        existing_book.title = book.title
        existing_book.subtitle = book.subtitle
        existing_book.description = book.description
        existing_book.isbn10 = book.isbn10.value
        existing_book.isbn13 = book.isbn13.value
        existing_book.publish_date = date.fromisoformat(book.publishDate.value)
        existing_book.number_of_pages = book.numberOfPages

        author_instances = [
            AuthorModel.objects.get_or_create(name=author)[0]
            for author in book.authors
        ]

        publisher_instances = [
            PublisherModel.objects.get_or_create(name=publisher)[0]
            for publisher in book.publishers
        ]

        existing_book.authors.set(author_instances)
        existing_book.publishers.set(publisher_instances)

        existing_book.save()

        return book_model_mapper.book_entity(existing_book)

    def delete(self, book_id: str) -> Book:
        book = BookModel.objects.get(id=book_id)

        deleted_book = book_model_mapper.book_entity(book)

        book.delete()

        return deleted_book
