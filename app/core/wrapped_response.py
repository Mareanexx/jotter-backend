from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class WrappedResponse(GenericModel, Generic[T]):
    message: Optional[str] = None
    data: Optional[T] = None
