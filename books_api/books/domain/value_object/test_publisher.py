import pytest

from .publisher import Publisher

def test_createPublisher_failWithoutName():
  with pytest.raises(ValueError) as e:
    Publisher(None)
  assert str(e.value) == "Publisher name is required", "Should fail without name"

def test_createPublisher_success():
  publisher = Publisher("Publisher name")
  assert publisher.name == "Publisher name", "Name should be 'Publisher name'"