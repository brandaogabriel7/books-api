from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)

from books.domain.factory.book_factory import book_factory

from books.infrastructure.models.book_model import BookModel

from books.application.service.book_service import BookService
from books.infrastructure.open_library.open_library_client import (
    OpenLibraryClient,
)
from books.domain.entity.book import Book

repository = DjangoBookRepository()
book_service = BookService(OpenLibraryClient())


@api_view(["GET", "POST"])
def book_list(request: Request):
    if request.method == "GET":
        return __list_books(request.query_params)

    if request.method == "POST":
        return __create_book(request.data)

    return Response(status=405)


@api_view(["GET", "PUT", "DELETE"])
def book_details(request, book_id):
    if request.method == "GET":
        return __get_book(book_id)

    if request.method == "PUT":
        return __update_book(book_id, request.data)

    if request.method == "DELETE":
        return __delete_book(book_id)

    return Response(status=405)


def __build_filters(query):
    if "isbn" in query:
        return {"isbn": query.get("isbn")}

    filters = {}

    if "title" in query:
        filters["title"] = query.get("title")
    if "subtitle" in query:
        filters["subtitle"] = query.get("subtitle")
    if "description" in query:
        filters["description"] = query.get("description")
    if "authors" in query:
        filters["authors"] = query.getlist("authors")
    if "publishers" in query:
        filters["publishers"] = query.getlist("publishers")
    if "publishDate" in query:
        filters["publishDate"] = query.get("publishDate")
    if "numberOfPages" in query:
        filters["numberOfPages"] = query.get("numberOfPages")

    return filters


def __list_books(query):
    page = query.get("page", 1)
    page_size = query.get("page_size", 10)
    filters = __build_filters(query)

    books = repository.list(page=page, page_size=page_size, filters=filters)

    return Response([__build_book_response(book) for book in books])


def __create_book(data):
    book = book_factory(data)

    book = book_service.enrich_book_data(book)

    created_book = repository.create(book)

    return Response(
        status=201,
        data=__build_book_response(created_book),
    )


def __get_book(book_id):
    try:
        book = repository.get(book_id)

        return Response(__build_book_response(book))

    except BookModel.DoesNotExist:
        return Response(status=404)


def __update_book(book_id, data):
    try:
        book = book_factory(data)

        book = book_service.enrich_book_data(book)

        updated_book = repository.update(str(book_id), book)

        return Response(__build_book_response(updated_book))

    except BookModel.DoesNotExist:
        return Response(status=404)


def __delete_book(book_id):
    try:
        deleted_book = repository.delete(book_id)

        return Response(__build_book_response(deleted_book))

    except BookModel.DoesNotExist:
        return Response(status=404)


def __build_book_response(book: Book):
    return {
        "id": book.id,
        "title": book.title,
        "subtitle": book.subtitle,
        "description": book.description,
        "authors": book.authors,
        "publishers": book.publishers,
        "isbn10": (book.isbn10.value if book.isbn10 else None),
        "isbn13": (book.isbn13.value if book.isbn13 else None),
        "publishDate": (book.publishDate.value if book.publishDate else None),
        "numberOfPages": book.numberOfPages,
    }
