class ValidationError(Exception):
  """A Validation Error raised from a Type or ValueError"""
  def __init__(self, *args):
      """
        Initialize a ValidationError.
        
        Args:
            message: A summary message for the group of errors.
            error: 
        """
      super().__init__(*args)

class ValidationErrorGroup(ValidationError):
    """A group of validation errors encountered during recursive validation."""
    
    def __init__(self, message: str, errors: list[tuple[object, ValidationError]]) -> None:
        """
        Initialize a ValidationErrorGroup.
        
        Args:
            message: A summary message for the group of errors.
            errors: A list of (object, error) tuples where each error was encountered.
        """
        super().__init__(message)
        self.errors = errors
        
    def __str__(self) -> str:
        result = [super().__str__()]
        for i, (obj, error) in enumerate(self.errors, 1):
            result.append(f"  {i}. In {obj.__class__.__name__}: {error}")
        return "\n".join(result)