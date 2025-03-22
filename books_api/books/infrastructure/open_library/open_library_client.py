import requests
from datetime import datetime


class OpenLibraryClient:
    def __init__(self):
        self.__base_url = "https://openlibrary.org"

    def get_book_info(self, isbn: str) -> dict:
        try:
            response = requests.get(
                f"{self.__base_url}/api/volumes/brief/isbn/{isbn}.json",
                headers={"Accept": "application/json"},
            )

            if response.status_code != 200:
                return None

            records = response.json().get("records", {})
            if not records:
                return None

            data = records.get(list(records.keys())[0], {}).get("data", {})
            if not data:
                return None

            title = data.get("title", "")
            subtitle = data.get("subtitle", "")

            authors = [
                author.get("name", "") for author in data.get("authors", [])
            ]
            publishers = [
                publisher.get("name", "")
                for publisher in data.get("publishers", [])
            ]

            identifiers = data.get("identifiers", {})
            isbn10 = identifiers.get("isbn_10", [""])[0]
            isbn13 = identifiers.get("isbn_13", [""])[0]

            publish_date = data.get("publish_date", "")
            try:
                publishDate = (
                    datetime.strptime(publish_date, "%d %B %Y")
                    .date()
                    .isoformat()
                    if publish_date
                    else ""
                )
            except ValueError:
                publishDate = ""

            numberOfPages = data.get("number_of_pages", 0)

            details = records.get(list(records.keys())[0], {}).get(
                "details", {}
            )
            workKey = (
                details.get("details", {}).get("works", [{}])[0].get("key", "")
            )

            return {
                "title": title,
                "subtitle": subtitle,
                "authors": authors,
                "publishers": publishers,
                "isbn10": isbn10,
                "isbn13": isbn13,
                "publishDate": publishDate,
                "numberOfPages": numberOfPages,
                "workKey": workKey,
            }

        except Exception as e:
            return None

    def get_book_work(self, workKey: str) -> dict:
        try:
            response = requests.get(
                f"{self.__base_url}{workKey}.json",
                headers={"Accept": "application/json"},
            )

            if response.status_code != 200:
                return None

            description = (
                response.json().get("description", {}).get("value", "")
            )

            return {
                "description": description,
            }
        except Exception:
            return None
