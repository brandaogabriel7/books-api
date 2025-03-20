class Author:
  def __init__(self, name):
    if name is None:
      raise ValueError("Author name is required")
    self.name = name