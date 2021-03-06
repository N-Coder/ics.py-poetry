import abc
import inspect
from typing import Dict, Generic, Iterable, Type, TypeVar

from ics.types import ContextDict, EmptyContext, EmptyParams, ExtraParams

T = TypeVar('T')


class ValueConverter(Generic[T], abc.ABC):
    BY_NAME: Dict[str, "ValueConverter"] = {}
    BY_TYPE: Dict[Type, "ValueConverter"] = {}
    INST: "ValueConverter"

    def __init_subclass__(cls) -> None:
        super(ValueConverter, cls).__init_subclass__()
        # isabstract(ValueConverter) == False on python 3.6
        if not inspect.isabstract(cls) and cls.parse is not ValueConverter.parse:
            cls.INST = cls()
            ValueConverter.BY_NAME[cls.INST.ics_type] = cls.INST
            ValueConverter.BY_TYPE.setdefault(cls.INST.python_type, cls.INST)

    @property
    @abc.abstractmethod
    def ics_type(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def python_type(self) -> Type[T]:
        pass

    def split_value_list(self, values: str) -> Iterable[str]:
        yield from values.split(",")

    def join_value_list(self, values: Iterable[str]) -> str:
        return ",".join(values)

    @abc.abstractmethod
    def parse(self, value: str, params: ExtraParams = EmptyParams, context: ContextDict = EmptyContext) -> T:
        pass

    @abc.abstractmethod
    def serialize(self, value: T, params: ExtraParams = EmptyParams, context: ContextDict = EmptyContext) -> str:
        pass

    def __str__(self):
        return "<" + self.__class__.__name__ + ">"

    def __hash__(self):
        return hash(type(self))
