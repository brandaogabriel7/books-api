from rest_framework.response import Response
from rest_framework.decorators import api_view

from books.infrastructure.repository.django_book_repository import (
    DjangoBookRepository,
)

repository = DjangoBookRepository()


@api_view(["GET", "POST"])
def book_list(request):
    if request.method == "GET":
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)
        filters = __build_filters(request.query_params)

        print(filters)

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

    elif request.method == "POST":
        return Response()


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
