from typing import Generic, TypedDict, TypeVar

T = TypeVar('T')


class SpriteForms(TypedDict, Generic[T]):
    normal: T
    shiny: T
