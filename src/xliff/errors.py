from typing import Any, Optional, TypedDict


class ErrorDetails(TypedDict):
  source: object
  attribute: str
  expected: type | tuple[type, ...] | str
  value: Any


class ValidationError(Exception):
  """A Validation Error raised from a Type or ValueError"""

  def __init__(self, error: Exception, details: ErrorDetails):
    """
    Creates a ValidationError.

    Args:
        source_error:  The error that triggered the ValidationError.
        attribute: The name of the attribute that failed validation.
        value: The value that failed validation
    """
    match error:
      case TypeError():
        super().__init__(
          f"Validation for attribute {details['attribute']!r} failed because of a TypeError. {type(details['value'])!r} is not a valid type for {details['attribute']!r}, expected {details['expected']!r}"
        )
      case ValueError():
        super().__init__(
          f"Validation for attribute {details['attribute']!r} failed because of a ValueError. {details['value']!r} is not a valid Value for {details['attribute']!r}, expected {details['expected']!r}"
        )
      case _:
        raise error


class ValidationErrorGroup(Exception):
  """A group of validation errors encountered during recursive validation."""

  def __init__(
    self, errors: Optional[list[tuple[object, ValidationError]]] = None
  ) -> None:
    """
    Creates a ValidationErrorGroup.

    Args:
        errors: A list of (object, error) tuples where each error was encountered.
    """
    super().__init__()
    self.errors = [] if errors is None else errors

  def __str__(self) -> str:
    return "\n".join(
      (
        f"  {i}. In {obj.__class__.__name__}: {error}"
        for i, (obj, error) in enumerate(self.errors, 1)
      )
    )
