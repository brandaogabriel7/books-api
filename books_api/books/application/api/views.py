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

    return Response(
        [
            {
                "id": book.id,
                "title": book.title,
                "subtitle": book.subtitle,
                "description": book.description,
                "authors": book.authors,
                "publishers": book.publishers,
                "isbn10": book.isbn10.value,
                "isbn13": book.isbn13.value,
                "publishDate": book.publishDate.value,
                "numberOfPages": book.numberOfPages,
            }
            for book in books
        ]
    )


def __create_book(data):
    book = book_factory(data)

    book = book_service.enrich_book_data(book)

    created_book = repository.create(book)

    return Response(
        status=201,
        data={
            "id": created_book.id,
            "title": created_book.title,
            "subtitle": created_book.subtitle,
            "description": created_book.description,
            "authors": created_book.authors,
            "publishers": created_book.publishers,
            "isbn10": created_book.isbn10.value,
            "isbn13": created_book.isbn13.value,
            "publishDate": created_book.publishDate.value,
            "numberOfPages": created_book.numberOfPages,
        },
    )


def __get_book(book_id):
    try:
        book = repository.get(book_id)

        return Response(
            {
                "id": book.id,
                "title": book.title,
                "subtitle": book.subtitle,
                "description": book.description,
                "authors": book.authors,
                "publishers": book.publishers,
                "isbn10": book.isbn10.value,
                "isbn13": book.isbn13.value,
                "publishDate": book.publishDate.value,
                "numberOfPages": book.numberOfPages,
            }
        )

    except BookModel.DoesNotExist:
        return Response(status=404)


def __update_book(book_id, data):
    try:
        book = book_factory(data)

        book = book_service.enrich_book_data(book)

        updated_book = repository.update(str(book_id), book)

        return Response(
            {
                "id": updated_book.id,
                "title": updated_book.title,
                "subtitle": updated_book.subtitle,
                "description": updated_book.description,
                "authors": updated_book.authors,
                "publishers": updated_book.publishers,
                "isbn10": updated_book.isbn10.value,
                "isbn13": updated_book.isbn13.value,
                "publishDate": updated_book.publishDate.value,
                "numberOfPages": updated_book.numberOfPages,
            }
        )

    except BookModel.DoesNotExist:
        return Response(status=404)


def __delete_book(book_id):
    try:
        deleted_book = repository.delete(book_id)

        return Response(
            {
                "id": deleted_book.id,
                "title": deleted_book.title,
                "subtitle": deleted_book.subtitle,
                "description": deleted_book.description,
                "authors": deleted_book.authors,
                "publishers": deleted_book.publishers,
                "isbn10": deleted_book.isbn10.value,
                "isbn13": deleted_book.isbn13.value,
                "publishDate": deleted_book.publishDate.value,
                "numberOfPages": deleted_book.numberOfPages,
            },
        )

    except BookModel.DoesNotExist:
        return Response(status=404)
