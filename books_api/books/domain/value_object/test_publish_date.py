import pytest

from books.domain.value_object.publish_date import PublishDate


@pytest.mark.parametrize("value", ["2021-01-01", "2023-11-30"])
def test_publishDate_success(value: str):

    publish_date = PublishDate(value)
    assert publish_date.value == value, f"Publish date should be '{value}'"


@pytest.mark.parametrize("invalidValue", [None, "", "2021-01-32", "2023-11-00"])
def test_publishDate_invalid(invalidValue: str):
    with pytest.raises(ValueError):
        PublishDate(invalidValue)


@pytest.mark.parametrize("futureDate", ["9999-12-31", "3000-01-01"])
def test_publishDate_cannotBeFuture(futureDate):
    with pytest.raises(ValueError):
        PublishDate(futureDate)
