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

            records = response.json()["records"]
            data = records[list(records.keys())[0]]["data"]

            title = data["title"]
            subtitle = data["subtitle"]

            authors = [author["name"] for author in data["authors"]]
            publishers = [publisher["name"] for publisher in data["publishers"]]

            isbn10 = data["identifiers"]["isbn_10"][0]
            isbn13 = data["identifiers"]["isbn_13"][0]

            publishDate = (
                datetime.strptime(data["publish_date"], "%d %B %Y")
                .date()
                .isoformat()
            )

            numberOfPages = data["number_of_pages"]

            details = records[list(records.keys())[0]]["details"]
            workKey = details["details"]["works"][0]["key"]

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

        except Exception:
            return None

    def get_book_work(self, workKey: str) -> dict:
        try:
            response = requests.get(
                f"{self.__base_url}{workKey}.json",
                headers={"Accept": "application/json"},
            )

            if response.status_code != 200:
                return None

            description = response.json()["description"]["value"]

            return {
                "description": description,
            }
        except Exception:
            return None
