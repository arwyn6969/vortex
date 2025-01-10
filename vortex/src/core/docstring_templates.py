"""Templates and examples for consistent docstring formatting across the codebase."""

from typing import Any, Dict, List, Optional, Tuple, Union

def function_template(arg1: Any, arg2: Optional[str] = None) -> Dict[str, Any]:
    """
    Brief description of the function's purpose.
    
    Detailed description of the function's behavior, including any important
    notes about implementation, edge cases, or assumptions.
    
    Args:
        arg1: Description of first argument
        arg2: Description of second argument, noting it's optional
        
    Returns:
        Description of return value and its structure
        
    Raises:
        ExceptionType: Description of when this exception is raised
        AnotherError: Description of another possible error condition
        
    Example:
        >>> result = function_template(42, "test")
        >>> print(result)
        {'value': 42, 'text': 'test'}
    """
    pass

class ClassTemplate:
    """
    Brief description of the class's purpose.
    
    Detailed description of the class's behavior and responsibilities.
    Include any important notes about usage patterns or assumptions.
    
    Attributes:
        attr1 (type): Description of first attribute
        attr2 (type): Description of second attribute
        
    Example:
        >>> obj = ClassTemplate()
        >>> obj.method_name()
        Expected output
    """
    
    def __init__(self, param1: str, param2: int = 0) -> None:
        """
        Initialize the class instance.
        
        Args:
            param1: Description of first parameter
            param2: Description of second parameter, noting default value
            
        Raises:
            ValueError: If param1 is empty
        """
        pass
        
    def method_template(
        self,
        arg1: List[str],
        *,
        kwarg1: Optional[bool] = None
    ) -> Tuple[int, str]:
        """
        Brief description of the method's purpose.
        
        Detailed description of the method's behavior.
        
        Args:
            arg1: Description of first argument
            kwarg1: Description of first keyword-only argument
            
        Returns:
            Tuple containing:
                - int: Description of first tuple element
                - str: Description of second tuple element
                
        Raises:
            ValueError: Description of error condition
        """
        pass

def property_template() -> str:
    """
    Brief description of the property.
    
    Detailed description of what the property represents and how it's computed.
    
    Returns:
        Description of the property value
        
    Raises:
        AttributeError: If accessed before initialization
    """
    pass

def generator_template(items: List[Any]) -> Any:
    """
    Brief description of the generator.
    
    Detailed description of what the generator produces and how it works.
    
    Args:
        items: Description of input sequence
        
    Yields:
        Description of each yielded value
        
    Raises:
        StopIteration: When the sequence is exhausted
    """
    pass

def async_template(resource_id: str) -> Any:
    """
    Brief description of the async function.
    
    Detailed description of the async operation and its behavior.
    
    Args:
        resource_id: Description of resource identifier
        
    Returns:
        Description of the awaited result
        
    Raises:
        ConnectionError: If resource is unavailable
        
    Example:
        >>> async def main():
        ...     result = await async_template("resource1")
        ...     print(result)
    """
    pass

# Example usage of type hints
ComplexType = Union[Dict[str, Any], List[Tuple[str, int]]]

def type_hint_template(
    simple_arg: int,
    complex_arg: ComplexType,
    optional_arg: Optional[str] = None,
    *args: Any,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Example of comprehensive type hint usage.
    
    Shows various ways to use type hints with documentation.
    
    Args:
        simple_arg: A simple integer argument
        complex_arg: A more complex argument with Union type
        optional_arg: An optional string argument
        *args: Variable positional arguments
        **kwargs: Variable keyword arguments
        
    Returns:
        A dictionary containing processed results
        
    Raises:
        TypeError: If arguments have incorrect types
    """
    pass 